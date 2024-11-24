from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(validation_alias="database_url")

    aws_s3_bucket: str = Field(validation_alias="aws_s3_bucket")
    aws_region: str = Field(validation_alias="aws_region")
    openai_api_key: str = Field(validation_alias="openai_api_key")
    retell_ai_api_key: str = Field(validation_alias="retell_ai_api_key")
    retell_ai_agent_id: str = Field(validation_alias="retell_ai_agent_id")

    @property
    def aws_s3_bucket_url(self) -> str:
        return f"https://{self.aws_s3_bucket}.s3.us-west-1.amazonaws.com"


settings = Settings()  # type: ignore
