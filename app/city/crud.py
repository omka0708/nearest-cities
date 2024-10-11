from sqlalchemy import select, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import models, schemas
from app.utils import geocode, get_distance


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> str:
    """
    Добавить города в хранилище

    :param db: подключение к БД
    :param city: город

    :return: статус (exist, not_exist, created)
    """
    city_dict = city.model_dump()

    existing_city = await get_city(city_title=city.title, db=db)
    if existing_city:
        return "exist"

    geocoded: dict = await geocode(address=city.title)
    if geocoded.get("geo_lat") is None or geocoded.get("geo_lon") is None or geocoded.get("qc") != 0:
        return "not_exist"

    city_dict["title"] = geocoded.get("result")
    city_dict["latitude"] = float(geocoded.get("geo_lat"))
    city_dict["longitude"] = float(geocoded.get("geo_lon"))

    db_city = models.City(**city_dict)
    db.add(db_city)
    await db.commit()
    return "created"


async def get_cities(db: AsyncSession) -> list[schemas.CityRead]:
    """
    Получить все города

    :param db: подключение к БД

    :return: города
    """
    db_cities = await db.execute(select(models.City))
    obj_cities = db_cities.scalars().all()
    result_schemas = [
        schemas.CityRead.model_validate(obj_city) for obj_city in obj_cities
    ]
    return result_schemas


async def get_city(
    db: AsyncSession, city_title: str | None, city_id: int | None = None
) -> schemas.CityRead | None:
    """
    Получить город (по ID или названию)

    :param db: подключение к БД
    :param city_title: название города, в любой форме, опционально
    :param city_id: ID города, опционально

    :return: найденный город
    """
    if city_title is None and city_id is None:
        return

    statement = False

    if city_id:
        statement = models.City.id == city_id

    if city_title:
        geocoded = await geocode(address=city_title)
        if geocoded.get("result") is None:
            return
        statement = or_(
            models.City.id == city_id, models.City.title == geocoded.get("result")
        )

    db_city = await db.execute(select(models.City).where(statement))
    obj_city = db_city.scalar()
    if not obj_city:
        return

    return schemas.CityRead.model_validate(obj_city)


async def delete_city(
    db: AsyncSession, city_title: str | None, city_id: int | None = None
) -> str | None:
    """
    Удалить город (по ID или названию)

    :param db: подключение к БД
    :param city_title: название города, в любой форме, опционально
    :param city_id: ID города, опционально
    :return: статус (deleted)
    """
    city = await get_city(db=db, city_title=city_title, city_id=city_id)
    if not city:
        return

    await db.execute(
        delete(models.City).where(
            or_(models.City.id == city.id, models.City.title == city.title)
        )
    )

    await db.commit()
    return "deleted"


async def get_nearest_cities(
    db: AsyncSession, lat: float, lon: float, amount: int
) -> list[schemas.CityRead]:
    """
    Получить ближайшие города

    :param db: подключение к БД
    :param lat: широта
    :param lon: долгота
    :param amount: количество городов

    :return: ближайшие города
    """
    cities = await get_cities(db=db)
    nearest_cities = sorted(
        cities,
        key=lambda city: get_distance(
            lat_1=lat, lon_1=lon, lat_2=city.latitude, lon_2=city.longitude
        ),
    )
    return nearest_cities[:amount]
