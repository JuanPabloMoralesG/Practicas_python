import datetime

from pydantic import BaseModel, Field, field_validator


class Movie(BaseModel):
    id:int
    name:str
    rate:float
    year:int
    category:str

class Movie_update(BaseModel):
    name:str
    rate:float
    year:int
    category:str

class Movie_create(BaseModel):
    id: int
    name:str
    rate:float = Field(ge=0,le=10,default=0)
    year:int = Field(le=datetime.date.today().year, ge=1900)
    category:str =Field(min_length=5,max_length=10)

    model_config = {
        'json_schema_extra':{
            'example':{
                'id':0,
                'name':'new_name',
                'rate':0,
                'year':datetime.date.today().year,
                'category':'action'
            }
        }
    }

    @field_validator("name")
    def validate_title(cls,name):
        if len(name) < 5:
            raise ValueError("name must have at least 5 characters")
        if len(name) > 15:
            raise ValueError("name can't have more than 15 characters")
        return name