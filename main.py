#Python
from typing import Optional
from enum import Enum


#Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI, UploadFile
from fastapi import status, HTTPException
from fastapi import Body, Query, Path, Cookie, File, Header, Form  

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
    status_code = status.HTTP_201_CREATED,
    tags = ["Person"],
    summary = "Create person in the app"
    )
def create_person(person:Person = Body(...)):
    """
    Create a new person

    Tis path operation creates a person in the app save the information in the database
    
    Parameters:
    - Request body parameters
        - **person: Person** -> A person model first name, last name, age, hair color and marital status
    Returns a person model with first name, last name, age, hair color
    """
    return person
    


# Validations: QueryParameters

@app.get("/person/detail", status_code = status.HTTP_200_OK, tags = ["Person"])
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

person = [1, 2, 3, 4, 5]

@app.get("/person/detail/{person_id}", tags = ["Person"])
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example = 126
    )
):
    if person_id not in person:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "This person doesn't exist"
        ) 
    return {person_id: "It exists"}


# Validations: Request Body

@app.put("/person/{person_id}", tags = ["Person"])
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

# Forms

@app.post(
    "/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags = ["Person"]
)
def login(username:str = Form(...), password:str = Form(...)):
    return LoginOut(username=username)

# Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code = status.HTTP_200_OK
)
def contac(
    first_name:str = Form(
        ...,
        max_length = 20,
        min_length = 1,
    ),
    last_name:str = Form(
        ...,
        max_length = 20,
        min_length = 1,
    ),
    email:EmailStr = Form(...),
    message:str = Form(
        ...,
        min_length = 20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads:Optional[str] = Cookie(default=None)
):
    return user_agent

# FIle

@app.post("/post-image")
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read()) / 1024, ndigits=2)
    }