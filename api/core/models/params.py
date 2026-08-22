from pydantic import BaseModel, Field


class ShortenRequestParams(BaseModel):
    url: str = Field("", max_length=100)
    alias: str = Field("", max_length=50)
    availability_duration_mins: int = Field(60, ge=1)
