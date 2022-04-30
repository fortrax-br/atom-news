from dataclasses import dataclass


@dataclass
class Style:
    title_style: int | None = None
    service_style: int | None = None
    description_style: int | None = None


@dataclass
class User:
    id: int
    chat_id: int
    title_style: int
    service_style: int
    description_style: int


@dataclass
class Service:
    id: int
    url: str
    title: str
    last_update: int
