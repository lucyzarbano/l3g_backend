from __future__ import annotations

from sqlalchemy.orm import Session, selectinload

from models.entities import AboutSection


class AboutRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_active(self) -> AboutSection | None:
        return (
            self.db.query(AboutSection)
            .options(selectinload(AboutSection.paragraphs), selectinload(AboutSection.images))
            .filter(AboutSection.active.is_(True))
            .order_by(AboutSection.sort_order)
            .first()
        )
