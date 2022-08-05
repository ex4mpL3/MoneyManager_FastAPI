from fastapi import APIRouter

from wallet.api.auth import router as auth_router
from wallet.api.operations import router as operations_router
from wallet.api.reports import router as reports_router


router = APIRouter()
router.include_router(auth_router)
router.include_router(operations_router)
router.include_router(reports_router)
