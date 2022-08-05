from typing import List, Optional

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from wallet import tables
from wallet.database import get_session
from wallet.models.operations import (
    OperationKindEnum,
    OperationCreate,
    OperationUpdate,
)


class OperationsService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def __get(self, user_id: int, operation_id: int) -> tables.Operation:
        operation = (
            self.session
                .query(tables.Operation)
                .filter_by(
                    id=operation_id,
                    user_id=user_id,
                )
                .first()
        )
        if operation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"custom": "response"}
            )
        return operation

    def get_list(
            self,
            user_id: int,
            kind: Optional[OperationKindEnum] = None
    ) -> List[tables.Operation]:

        query = (
            self.session
                .query(tables.Operation)
                .filter_by(user_id=user_id)
        )

        if kind:
            query = query.filter_by(kind=kind)
        operations = query.all()
        return operations

    def get(self, user_id: int, operation_id: int) -> tables.Operation:
        return self.__get(user_id=user_id, operation_id=operation_id)

    def create_many(self,
                    user_id: int,
                    operations_data: List[OperationCreate],
                    ) -> List[tables.Operation]:

        operations = [
            tables.Operation(
                **operation_data.dict(),
                user_id=user_id,
            )
            for operation_data in operations_data
        ]
        self.session.add_all(operations)
        self.session.commit()

        return operations

    def create(
            self,
            user_id: int,
            operation_data: OperationCreate
    ) -> tables.Operation:

        operation = tables.Operation(
            **operation_data.dict(),
            user_id=user_id,
        )
        self.session.add(operation)
        self.session.commit()

        return operation

    def update(self,
               user_id: int,
               operation_id: int,
               operation_data: OperationUpdate,
               ) -> tables.Operation:
        operation = self.__get(user_id=user_id, operation_id=operation_id)
        for field, value in operation_data:
            setattr(operation, field, value)  # update fields

        self.session.commit()
        return operation

    def delete(self, user_id: int, operation_id: int):
        operation = self.__get(user_id=user_id, operation_id=operation_id)
        self.session.delete(operation)
        self.session.commit()
