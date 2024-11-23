from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(validation_alias="database_url")

    aws_s3_bucket: str = Field(validation_alias="aws_s3_bucket")
    aws_region: str = Field(validation_alias="aws_region")
    openai_api_key: str = Field(validation_alias="openai_api_key")


settings = Settings()  # type: ignore
