from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(validation_alias="database_url")

    alembic_ini_path: str = str(Path(__file__).parent.parent / "alembic.ini")
    aws_s3_bucket: str = Field(validation_alias="aws_s3_bucket")
    aws_region: str = Field(validation_alias="aws_region")


settings = Settings()  # type: ignore
