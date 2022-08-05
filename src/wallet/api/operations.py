from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from wallet.models.auth import User
from wallet.models.operations import (
    Operation,
    OperationKindEnum,
    OperationCreate,
    OperationUpdate,
)
from wallet.services.auth import get_current_user
from wallet.services.operations import OperationsService

router = APIRouter(
    prefix='/operations',
    tags=['operations'],
)


@router.get('/',
            response_model=List[Operation])
def get_operation_list(
        kind: Optional[OperationKindEnum] = None,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    """
    Get list operations.
    - **kind**: filter by type operation.
    \f
    :param kind:
    :param user:
    :param service:
    :return:
    """
    return service.get_list(user_id=user.id, kind=kind)


@router.post('/', response_model=Operation)
def create_operation(
        operation_data: OperationCreate,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    """Create new operation"""
    return service.create(user_id=user.id, operation_data=operation_data)


@router.get('/{operation_id}', response_model=Operation)
def get_operation(
        operation_id: int,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    """Get operation by id"""
    return service.get(user_id=user.id, operation_id=operation_id)


@router.put('/{operation_id}', response_model=Operation)
def update_operation(
        operation_id: int,
        operation_data: OperationUpdate,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    """Update operation"""
    return service.update(
        user_id=user.id,
        operation_id=operation_id,
        operation_data=operation_data,
    )


@router.delete('/{operation_id}')
def delete_operation(
        operation_id: int,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    """Delete operation"""
    service.delete(user_id=user.id, operation_id=operation_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
