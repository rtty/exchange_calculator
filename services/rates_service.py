import heapq
import math
from datetime import datetime
from http.client import HTTPException
from typing import List, Tuple

from sqlalchemy.orm import Session, joinedload

from db.models import Rate
from db.schemas import RateModel, RateCalcResponse, RateModelResponse
from services.currencies_service import get_currency_by_code_or_404


def save_rate(new_rate: RateModel, db: Session, id: int = None) -> RateCalcResponse:
    """
    Saves new currency exchange rate to the database.
    """
    base_currency = get_currency_by_code_or_404(new_rate.currency_base, db)
    target_currency = get_currency_by_code_or_404(new_rate.currency_target, db)

    if not id:
        # create new rate instance
        rate = Rate(
            currency_base_id=base_currency.id,
            currency_target_id=target_currency.id,
            rate=new_rate.rate,
            date=new_rate.date,
        )
        db.add(rate)
    else:
        # update rate instance
        rate = db.get(Rate, id)
        rate.rate = new_rate.rate
        rate.date = new_rate.date
        rate.currency_base_id=base_currency.id
        rate.currency_target_id=target_currency.id


    # save the rate to the database
    db.commit()
    db.refresh(rate)

    return rate


def delete_rate(id: int, db: Session) -> None:
    """
    Deletes currency exchange rate from the database.
    """
    rate = db.get(Rate, id)
    db.delete(rate)
    db.commit()


def get_all_rates(
    currency_base_code: str = None, currency_target_code: str = None, db: Session = None
) -> List[RateModelResponse]:
    """
    Retrieves list of currency exchange rates based on optional filters.
    """
    # start building the query
    query = db.query(Rate).options(joinedload(Rate.currency_base_rel), joinedload(Rate.currency_target_rel))

    # apply base currency filter if provided
    if currency_base_code:
        currency_base = get_currency_by_code_or_404(currency_base_code, db)
        query = query.filter_by(currency_base_id=currency_base.id)

    # apply target currency filter if provided
    if currency_target_code:
        currency_target = get_currency_by_code_or_404(currency_target_code, db)
        query = query.filter_by(currency_target_id=currency_target.id)

    return query.all()


def calculate_rate(graph: dict, start_currency: str, end_currency: str) -> Tuple[float, List[Tuple[str, str]]]:
    """
    Implements dijkstra's algorithm to find the minimum rate and optimal cross exchange pairs between two currencies.
    """

    # initialization of distances and paths
    distances = {currency: math.inf for currency in graph}
    paths = {currency: [] for currency in graph}
    distances[start_currency] = 1  # initial rate for the starting currency
    heap = [(1, start_currency)]

    while heap and distances[end_currency] == math.inf:
        current_rate, current_currency = heapq.heappop(heap)

        # iterate over neighbors of the current currency
        for neighbor, rate in graph[current_currency]:
            # calculate the new rate to reach the neighbor
            new_rate = current_rate * rate
            if new_rate < distances[neighbor]:
                distances[neighbor] = new_rate
                paths[neighbor] = paths[current_currency] + [(current_currency, neighbor)]
                heapq.heappush(heap, (new_rate, neighbor))
            elif new_rate == distances[neighbor]:
                paths[neighbor].extend(paths[current_currency] + [(current_currency, neighbor)])

    # if there is a path, return all found paths
    if not paths[end_currency]:
        return None, []
    else:
        return distances[end_currency], paths[end_currency]


def get_rate_by_date(currency_base: str, currency_target: str, date: datetime.date, db: Session = None) -> RateCalcResponse:
    """
    Gets the exchange rate and optimal cross exchange pairs between two currencies for a given date.
    """
    result = db.query(Rate).filter_by(date=date).all()

    if not result:
        raise HTTPException(404, f'No rates {currency_base}/{currency_target} for {date}.')

    data = [(r.currency_base, r.currency_target, r.rate) for r in result] + [
        (r.currency_target, r.currency_base, 1 / r.rate) for r in result
    ]
    # build the graph of currency pairs
    graph = {}
    for row in data:
        base, target, rate = row
        if base not in graph:
            graph[base] = []
        graph[base].append((target, rate))

    min_rate, optimal_paths = calculate_rate(graph, currency_base, currency_target)

    return RateCalcResponse(
        rate=min_rate,
        currency_base=currency_base,
        currency_target=currency_target,
        date=date,
        cross_pairs=optimal_paths,
    )
