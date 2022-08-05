from typing import TypeVar

from pydantic import BaseSettings

TIME_SECONDS = TypeVar('TIME_SECONDS', int, int)


class Settings(BaseSettings):

    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str

    report_file_name = 'report.csv'

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration: TIME_SECONDS = 3600


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
