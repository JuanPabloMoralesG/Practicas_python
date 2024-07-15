import datetime

from pydantic import BaseModel, Field, field_validator


class Movie(BaseModel):
    id:int
    name:str
    rate:float 
    year:int 
    category:str

    @field_validator("name")
    def validate_title(cls,name):
        if len(name) < 5:
            raise ValueError("name must have at least 5 characters")
        if len(name) > 15:
            raise ValueError("name can't have more than 15 characters")
        return name