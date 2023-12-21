from typing import List

from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from config import get_db
from db.schemas import CurrencyModel, CurrencyModelResponse, Message
from services import currencies_service

router = APIRouter(prefix='/currencies', tags=['currencies'])


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {'model': Message}},
)
def create_currency(currency: CurrencyModel, db: Session = Depends(get_db)) -> CurrencyModelResponse:
    """
    Endpoint to create new currency.
    """
    exists = currencies_service.get_currency_by_code(currency.code, db)
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Currency already registered')

    return currencies_service.create_currency(currency.code, db)


@router.put(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    responses={status.HTTP_409_CONFLICT: {'model': Message}},
)
def update_currency(id: int, currency: CurrencyModel, db: Session = Depends(get_db)) -> CurrencyModelResponse:
    """
    Endpoint to update an existing currency code.
    """
    return currencies_service.update_currency(id, currency.code, db)


@router.delete('/{currency_code}', status_code=status.HTTP_204_NO_CONTENT)
def delete_currency(currency_code: str, db: Session = Depends(get_db)) -> None:
    """
    Endpoint to delete currency code.
    """
    currencies_service.delete_currency(currency_code, db)


@router.get('/', response_model=List[CurrencyModelResponse])
def get_all_currencies(
    db: Session = Depends(get_db),
) -> List[CurrencyModelResponse]:
    """
    Endpoint to retrieve list of all currency codes.
    """
    return currencies_service.get_all_currencies(db)
