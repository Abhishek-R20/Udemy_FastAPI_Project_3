from pydantic import BaseModel, ConfigDict, Field

# from typing import Optional


class TodosBase(BaseModel):
    title: str
    description: str
    priority: int = Field(description="will be default 2 always ", default=2)
    complete: bool = Field(default=False)


# You don't need to write = Field() for every single attribute. If a field doesn't have extra validation (like a minimum length or a specific description), just use standard Python type hints. It makes your code much cleaner.


class TodosCreate(TodosBase):
    # id: Optional[int] = Field(
    #         description="Id is not mandatory, if provided with post request, it will be checked first",
    #         default=None,
    #     )
    pass


class TodosResponse(TodosBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
