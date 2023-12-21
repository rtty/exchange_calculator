from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config import get_db
from db.schemas import RateModel, RateCalcResponse, RateModelResponse
from services import rates_service

router = APIRouter(prefix='/rates', tags=['rates'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_rate(rate: RateModel, db: Session = Depends(get_db)) -> RateModelResponse:
    """
    Endpoint to create new currency exchange rate.
    """
    return rates_service.save_rate(rate, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_rate(id: int, rate: RateModel, db: Session = Depends(get_db)) -> RateModelResponse:
    """
    Endpoint to update currency exchange rate.
    """
    return rates_service.save_rate(rate, db, id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_rate(id: int, db: Session = Depends(get_db)) -> None:
    """
    Endpoint to delete currency exchange rate.
    """
    rates_service.delete_rate(id, db)


@router.get('/history/{currency_base}/{currency_target}')
def get_historical_rates(
    currency_base: str, currency_target: str, db: Session = Depends(get_db)
) -> List[RateModelResponse]:
    """
    Endpoint to retrieve historical rates for specific currency pair.
    """
    return rates_service.get_all_rates(currency_base, currency_target, db)


@router.get('/rate/{currency_base}/{currency_target}/{date}')
def get_rate_by_date(
    currency_base: str, currency_target: str, date: str, db: Session = Depends(get_db)
) -> RateCalcResponse:
    """
    Endpoint to calculate currency exchange rate for specific date.
    """
    return rates_service.get_rate_by_date(currency_base, currency_target, date, db)
