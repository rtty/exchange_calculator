from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import Currency


def create_currency(currency_code: str, db: Session) -> Currency:
    """
    Creates a new currency to the database.
    """
    currency = Currency(code=currency_code)
    db.add(currency)
    db.commit()
    db.refresh(instance=currency)
    return currency


def update_currency(id: int, currency_code: str, db: Session) -> Currency:
    """
    Updates the code of an existing currency in the database.
    """
    currency = db.get(Currency, id)
    if not currency:
        raise HTTPException(404, f'Currency with id {id} not found.')
    currency.code = currency_code
    db.commit()
    return currency


def delete_currency(currency_code: str, db: Session) -> None:
    """
    Deletes a currency from the database.
    """
    currency = get_currency_by_code(currency_code, db)
    if not currency:
        raise HTTPException(404, f'Currency {currency_code} not found.')
    db.delete(currency)
    db.commit()


def get_currency_by_code(code: str, db: Session) -> Currency:
    """
    Retrieves a currency by code from the database.
    """
    return db.query(Currency).filter_by(code=code).first()


def get_currency_by_code_or_404(code: str, db: Session) -> Currency:
    """
    Retrieves a currency by code from the database or raises HTTPException (404) if not found.
    """
    currency = get_currency_by_code(code, db)
    if not currency:
        raise HTTPException(404, f'Currency {code} not found.')
    return currency


def get_all_currencies(db: Session) -> List[Currency]:
    """
    Retrieves all currencies from the database.
    """
    return db.query(Currency).all()
