from fastapi import FastAPI

from wallet.api import router


tags_metadata = [
    {
        'name': 'auth',
        'description': 'Authorization and registration'
    },
    {
        'name': 'operations',
        'description': 'Work with operations'
    },
    {
        'name': 'reports',
        'description': 'Import and export of reports'
    },
]

app = FastAPI(
    title='Wallet',
    description='Accounting service for personal expenses and income',
    version='1.0.0',
    openapi_tags=tags_metadata,
)
app.include_router(router)
