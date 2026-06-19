from pydantic import BaseModel, Field


class TodoRequest(BaseModel):

    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    priority: int = Field(lt=10, gt=0)
    complete: bool = Field()
