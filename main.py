#Python
from typing import Optional
from enum import Enum


#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI, Form
from fastapi import status
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"


class Location(BaseModel):
    city: str
    state: str
    country: str

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example = "David"
    )
    last_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example = "Zapata"
    )
    age: int = Field(
        ...,
        gt = 0,
        le = 115,
        example = 24
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

class Person(PersonBase):
    password: str = Field(..., min_length=8)

    """ class Config:
        schema_extra = {
            "example": {
                "first_name": "David",
                "last_name": "Zpata",
                "age": 23,
                "hair_color": "blonde",
                "is_married": False
            }
        } """

class PersonOut(PersonBase):
    pass
    """ first_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example = "David"
    )
    last_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example = "Zapata"
    )
    age: int = Field(
        ...,
        gt = 0,
        le = 115,
        example = 24
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None) """

class LoginOut(BaseModel):
    username:str = Field(..., max_length = 20, example = '123')
    message:str = Field(default="Login Successful")


@app.get("/", status_code = status.HTTP_200_OK)
def home():
    return {"Hello": "world"}


# Request and Response Body

@app.post(
    "/person/new",
    response_model = PersonOut,
    status_code = status.HTTP_201_CREATED
    )
def create_person(person:Person = Body(...)):
    return person


# Validations: QueryParameters

@app.get("/person/detail", status_code = status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description= "This is person name, It is between 1 and 50 characters",
        example = "Pedro"
        ),
    age: int = Query(
        ...,
        title= "Person Age",
        description= "This is the person age. It is required",
        example = 25
        )
):
    return {name: age}


# Validations Path

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example = 126
        )
):
    return {person_id: "It exists"}


# Validations: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        gt = 0,
        title = "Person ID",
        description = "This is the person ID",
        example = 126
    ),
    person: Person = Body(...),
    #location: Location = Body(...)
):
    #results = person.dict()
    #results.update(location.dict())
    return person

#

@app.post(
    "/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username:str = Form(...), password:str = Form(...)):
    return LoginOut(username=username)