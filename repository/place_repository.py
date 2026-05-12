from __future__ import annotations

from sqlalchemy.orm import Session, selectinload

from abstractrepository.base_repository import ReadRepository
from models.entities import Place


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
