from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import requests
from typeguard import typechecked
from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Title:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=32, custom=pattern(r'[\w\s\d+-.,;!]+'))

    def __str__(self):
        return self.value


class Category(Enum):
    MUS = 'Music'
    SPO = 'Sport'
    DOC = 'Documentary'
    GAM = 'Game'
    MOV = 'Movie'
    OTH = 'Other'


@typechecked
@dataclass(frozen=True, order=True)
class Description:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=256, custom=pattern(r'[\w\s\d+-.,;!]+'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Author:
    id: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('id', self.id, min_value=1)

    def __str__(self):
        return self.id


@typechecked
@dataclass(frozen=True, order=True)
class Views:
    count: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('count', self.count, min_value=0)

    def __str__(self):
        return self.count


@typechecked
@dataclass(frozen=True, order=True)
class VideoDetails:
    id: int
    title: Title
    description: Description
    author_name: str
    category: Category
    views: Views

    def __str__(self):
        return 'Video'


@typechecked
@dataclass(frozen=True, order=True)
class VideoAPI:
    __api_server = 'http://localhost:8000/api/v1'

    def fetch_videos(self) -> Optional[List[VideoDetails]]:
        response = requests.get(url=f'{self.__api_server}/videos/')
        if response.status_code != 200:
            return None
        data = []
        for elem in response.json():
            data.append(VideoDetails(
                id=int(elem['id']),
                title=Title(value=elem['title']),
                description=Description(value=elem['description']),
                author_name=elem['author_name'],
                category=Category[elem['category']],
                views=Views(count=int(elem['views']))
            ))
        return data

    def fetch_video(self, selection) -> Optional[VideoDetails]:
        response = requests.get(url=f'{self.__api_server}/videos/{selection}')
        if response.status_code != 200:
            return None
        elem = response.json()
        return VideoDetails(
            id=int(elem['id']),
            title=Title(value=elem['title']),
            description=Description(value=elem['description']),
            author_name=elem['author_name'],
            category=Category[elem['category']],
            views=Views(count=int(elem['views']))
        )

    def fetch_own_videos(self, key) -> Optional[List[VideoDetails]]:
        response = requests.get(url=f'{self.__api_server}/videos/own', headers={'Authorization': f'Token {key}'})
        if response.status_code != 200:
            return None
        data = []
        for elem in response.json():
            data.append(VideoDetails(
                id=int(elem['id']),
                title=Title(value=elem['title']),
                description=Description(value=elem['description']),
                author_name=elem['author_name'],
                category=Category[elem['category']],
                views=Views(count=int(elem['views']))
            ))
        return data
