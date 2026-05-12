from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LoginRequestSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class ImageSchema(BaseModel):
    src: str
    alt: str


class ServiceSchema(BaseModel):
    description: str
    icon_key: str


class RoomBadgeSchema(BaseModel):
    label: str


class RoomSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    short_description: str
    cover_image: ImageSchema
    link: str
    rate: float
    price_base: float | None
    capacity: int | None
    visible_in_home: bool
    reverse_layout: bool
    active: bool
    images: list[ImageSchema] = []
    services_base: list[ServiceSchema] = []
    services_additional: list[ServiceSchema] = []
    badges: list[str] = []


class RoomAdminSchema(BaseModel):
    id: str
    nome: str
    descrizione: str
    prezzoBase: float
    capienza: int
    immagineCopertina: str
    servizi: list[str] = []
    attiva: bool


class PlaceInfoItemSchema(BaseModel):
    icon_key: str
    title: str
    type: str
    description: str


class PlaceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    details_title: str
    description: str
    cover_image: ImageSchema
    event_date: str | None
    address: str | None
    distance_km: float | None
    category: str | None
    active: bool
    images: list[ImageSchema] = []
    info: list[PlaceInfoItemSchema] = []


class AboutImageSchema(BaseModel):
    src: str
    alt: str
    class_name: str | None = None


class AboutSchema(BaseModel):
    id: str
    eyebrow: str
    title: str
    description: list[str]
    images: list[AboutImageSchema]
