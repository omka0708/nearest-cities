from http.client import responses
from typing import Annotated

from fastapi import APIRouter, Depends, Response, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import crud, schemas
from app.database import get_async_session

router = APIRouter()


@router.post("/create")
async def create_city(
    title: Annotated[str, Form()],
    session: AsyncSession = Depends(get_async_session),
):
    city = schemas.CityCreate(title=title)
    result: str = await crud.create_city(city=city, db=session)
    if result == "created":
        return Response(status_code=201)
    elif result == "exist":
        raise HTTPException(
            status_code=409,
            detail={"status": "error", "msg": f"Город уже был добавлен в хранилище"},
        )
    else:  # == "not_exist"
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "msg": f"Города {title} не существует"},
        )


@router.get("/get/all", response_model=list[schemas.CityRead])
async def get_cities(
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.get_cities(db=session)


@router.get("/get", response_model=schemas.CityRead)
async def get_city(
    city_id: int | None = None,
    title: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    if city_id is None and title is None:
        raise HTTPException(
            status_code=422,
            detail={"status": "error", "msg": f"Необходимо передать city_id или title"},
        )
    city = await crud.get_city(db=session, city_title=title, city_id=city_id)
    if city:
        return city
    else:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "msg": f"Города нет в хранилище"},
        )


@router.delete("/delete", response_model=schemas.CityRead)
async def delete_city(
    city_id: int | None = None,
    title: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    if city_id is None and title is None:
        raise HTTPException(
            status_code=422,
            detail={"status": "error", "msg": f"Необходимо передать city_id или title"},
        )
    result = await crud.delete_city(db=session, city_title=title, city_id=city_id)
    if not result:  # != "deleted"
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "msg": f"Города нет в хранилище"},
        )
    return Response(status_code=204)


@router.get("/get/nearest", response_model=list[schemas.CityRead])
async def get_nearest_cities(
    lat: float,
    lon: float,
    amount: int = 2,
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.get_nearest_cities(db=session, lat=lat, lon=lon, amount=amount)
