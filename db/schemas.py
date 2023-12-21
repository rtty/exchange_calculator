import datetime
from typing import List, Tuple

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
)


# validation schemes
class Message(BaseModel):
    message: str


CURRENCY_CODE = Field(min_length=3, max_length=3, examples=['USD', 'EUR', 'GBP'])


class CurrencyModel(BaseModel):
    code: str = CURRENCY_CODE


class CurrencyModelResponse(CurrencyModel):
    id: int


class RateModel(BaseModel):
    rate: float
    currency_base: str = CURRENCY_CODE
    currency_target: str = CURRENCY_CODE
    date: datetime.date

    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, value: str) -> datetime.date:
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()

    @model_validator(mode='after')
    def check_currencies(self) -> 'RateModel':
        if self.currency_base == self.currency_target:
            raise ValueError('Currencies must be different')
        return self


class RateModelResponse(BaseModel):
    id: int
    rate: float
    currency_base: str = CURRENCY_CODE
    currency_target: str = CURRENCY_CODE
    date: datetime.date


class RateCalcResponse(BaseModel):
    rate: float
    currency_base: str = CURRENCY_CODE
    currency_target: str = CURRENCY_CODE
    date: datetime.date
    cross_pairs: List[Tuple[str, str]]
