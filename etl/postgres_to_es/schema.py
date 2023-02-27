from typing import List
from pydantic import BaseModel
from typing import Union


class InformationFilmCrew(BaseModel):
    id: str
    name: str


class Films(BaseModel):
    id: str
    imdb_rating: Union[float, None]
    genre: list
    title: str
    description: Union[str, None]
    director: str
    actors_names: str
    writers_names: str
    actors: List[InformationFilmCrew]
    writers: List[InformationFilmCrew]


class SchemaInformFilms(BaseModel):
    mappings: List[Films]
