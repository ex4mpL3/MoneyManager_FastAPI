from datetime import date
from enum import Enum
from typing import Optional

from pydantic import (
    BaseModel,
    condecimal,
    NonNegativeInt,
    constr
)


class OperationKindEnum(str, Enum):
    INCOME = 'income'
    OUTCOME = 'outcome'


class OperationBase(BaseModel):
    date: date
    kind: OperationKindEnum
    amount: condecimal(max_digits=10,
                       decimal_places=2)
    description: Optional[constr(strip_whitespace=True)]


class Operation(OperationBase):
    """Scheme for GET"""
    id: NonNegativeInt

    class Config:
        orm_mode = True


class OperationCreate(OperationBase):
    """Scheme for POST
    For future expansion
    """
    pass


class OperationUpdate(OperationBase):
    """
    Scheme for POST
    For future expansion
    """
    pass
