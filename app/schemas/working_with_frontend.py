from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class Cat(BaseModel):
    name: str
    meow_volume: int


class Dog(BaseModel):
    name: str
    bark_volume: int


class Ant(BaseModel):
    name: str
    ant_type: str


class Ants(BaseModel):
    ant_list: list[Ant] = Field(..., description="List of Ant")


class Bee(BaseModel):
    name: str
    bee_type: str


class AnimalHouseUnusualResponse(BaseModel):
    creature: Cat | Dog | list[Bee]
    mammalia: Cat | Dog


class AnimalHouseCommonResponse(BaseModel):
    creature: Cat | Dog | Ants
    mammalia: Cat | Dog
