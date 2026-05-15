from __future__ import annotations

from sqlalchemy.orm import Session, selectinload

from abstractrepository.base_repository import ReadRepository
from models.entities import Place, PlaceImage


class PlaceRepository(ReadRepository[Place]):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> list[Place]:
        return (
            self.db.query(Place)
            .options(selectinload(Place.images), selectinload(Place.info_items))
            .order_by(Place.sort_order, Place.title)
            .all()
        )

    def get_by_id(self, item_id: str) -> Place | None:
        return (
            self.db.query(Place)
            .options(selectinload(Place.images), selectinload(Place.info_items))
            .filter(Place.id == item_id)
            .first()
        )

    def exists(self, item_id: str) -> bool:
        return self.db.query(Place.id).filter(Place.id == item_id).first() is not None

    def add(self, place: Place) -> Place:
        self.db.add(place)
        self.db.commit()
        return self.get_by_id(place.id) or place

    def update(self) -> None:
        self.db.commit()

    def delete(self, place: Place) -> None:
        self.db.delete(place)
        self.db.commit()

    def replace_cover_image(self, place: Place, src: str, alt: str) -> None:
        cover = min(place.images, key=lambda image: image.sort_order, default=None)
        if cover is None:
            cover = PlaceImage(place_id=place.id, src=src, alt=alt, sort_order=1)
            self.db.add(cover)
        else:
            cover.src = src
            cover.alt = alt
