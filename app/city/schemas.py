from pydantic import BaseModel, ConfigDict


class CityCreate(BaseModel):
    title: str


class CityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    latitude: float
    longitude: float
