from math import cos, asin, sqrt
from httpx import HTTPStatusError
from dadata import DadataAsync

from .config import DADATA_API_KEY, DADATA_SECRET_KEY


async def geocode(address: str) -> dict:
    """
    Геокодировать адрес

    :param address: адрес
    :return: гео ответ DaData API
    """
    dadata = DadataAsync(DADATA_API_KEY, DADATA_SECRET_KEY)
    try:
        result = await dadata.clean("address", address)
    except HTTPStatusError:
        return {}
    return result


def get_distance(lat_1: float, lon_1: float, lat_2: float, lon_2: float) -> float:
    """
    Получить дистанцию по формуле Хаверсина
    https://en.wikipedia.org/wiki/Haversine_formula

    :param lat_1: широта в первой точке
    :param lon_1: долгота в первой точке
    :param lat_2: широта во второй точке
    :param lon_2: долгота во второй точке

    :return: дистанция (км)
    """
    p = 0.017453292519943295
    hav = (
        0.5
        - cos((lat_2 - lat_1) * p) / 2
        + cos(lat_1 * p) * cos(lat_2 * p) * (1 - cos((lon_2 - lon_1) * p)) / 2
    )
    return 12742 * asin(sqrt(hav))
