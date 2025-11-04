from fastapi import APIRouter

from app.schemas.working_with_frontend import (
    AnimalHouseCommonResponse,
    AnimalHouseUnusualResponse,
    Ant,
    Ants,
    Bee,
    Dog,
)

router = APIRouter()


@router.get("/union/common-response")
async def get_common_response() -> AnimalHouseCommonResponse:
    res = AnimalHouseCommonResponse(
        creature=Ants(
            ant_list=[
                Ant(name="Anty", ant_type="Leafcutter"),
                Ant(name="Tiny", ant_type="Fire"),
            ]
        ),
        mammalia=Dog(name="Rex", bark_volume=7),
    )
    return res


@router.get("/union/unusual-response")
async def get_unusual_response() -> AnimalHouseUnusualResponse:
    res = AnimalHouseUnusualResponse(
        creature=[
            Bee(name="Buzz", bee_type="Honeybee"),
            Bee(name="Sting", bee_type="Bumblebee"),
        ],
        mammalia=Dog(name="Rex", bark_volume=7),
    )
    return res
