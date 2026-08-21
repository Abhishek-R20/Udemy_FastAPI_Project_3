from pydantic import BaseModel, ConfigDict, Field

# from typing import Optional


class TodosBase(BaseModel):
    title: str
    description: str
    priority: int = Field(ge=1, le=5)
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


# class TodosUpdate(BaseModel):
#     title: str | None = Field(default=None)
#     description: str | None = Field(default=None)
#     priority: int | None = Field(default=None)
#     complete: bool | None = Field(default=None)


# 2. Unnecessary Boilerplate Writing = Field(default=None) does exactly the same thing behind the scenes as just writing = None. Unless you are explicitly using Field() to add extra rules (like description, ge, le, or max_length), you are just forcing yourself to type more code.


class TodosUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    complete: bool | None = None
    priority: int | None = Field(
        ge=1,
        le=5,
        default=5,
        description="Optional. Only send to update existing priority.",
    )
