from fastapi import (
    APIRouter,
    BackgroundTasks,
    UploadFile,
    File,
    Depends,
)
from fastapi.responses import StreamingResponse

from wallet.models.auth import User
from wallet.services.auth import get_current_user
from wallet.services.reports import ReportService
from wallet.settings import Settings
router = APIRouter(
    prefix='/reports',
    tags=['reports'],
)


@router.post('/import')
def import_csv(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        user: User = Depends(get_current_user),
        reports_service: ReportService = Depends(),
):
    """Upload CSV-file with info about operations"""
    background_tasks.add_task(
        reports_service.import_csv,
        user.id,
        file.file,
    )


@router.post('/export')
def export_csv(
        user: User = Depends(get_current_user),
        reports_service: ReportService = Depends(),
):
    """Download CSV-file with info about operations"""
    report = reports_service.export_csv(user_id=user.id)
    return StreamingResponse(
        content=report,
        media_type='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename={Settings.report_file_name}'
        },
    )


