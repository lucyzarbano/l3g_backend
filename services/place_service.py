from __future__ import annotations

from models.entities import Place
from models.schemas import ImageSchema, PlaceInfoItemSchema, PlaceSchema
from repository.place_repository import PlaceRepository


class PlaceService:
    def __init__(self, repository: PlaceRepository) -> None:
        self.repository = repository

    def list_places(self) -> list[PlaceSchema]:
        return [self._to_schema(place) for place in self.repository.list()]

    def get_place(self, place_id: str) -> PlaceSchema | None:
        place = self.repository.get_by_id(place_id)
        if place is None:
            return None
        return self._to_schema(place)

    def _to_schema(self, place: Place) -> PlaceSchema:
        return PlaceSchema(
            id=place.id,
            title=place.title,
            details_title=place.details_title,
            description=place.description,
            cover_image=ImageSchema(src=place.cover_image_src, alt=place.cover_image_alt),
            event_date=place.event_date,
            address=place.address,
            distance_km=float(place.distance_km) if place.distance_km is not None else None,
            category=place.category,
            active=place.active,
            images=[
                ImageSchema(src=image.src, alt=image.alt)
                for image in sorted(place.images, key=lambda item: item.sort_order)
            ],
            info=[
                PlaceInfoItemSchema(
                    icon_key=item.icon_key,
                    title=item.title,
                    type=item.type,
                    description=item.description,
                )
                for item in sorted(place.info_items, key=lambda item: item.sort_order)
            ],
        )
