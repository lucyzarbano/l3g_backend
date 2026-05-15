from __future__ import annotations

from models.entities import Place
from models.schemas import ImageSchema, PlaceAdminSchema, PlaceInfoItemSchema, PlaceSchema
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

    def list_admin_places(self) -> list[PlaceAdminSchema]:
        return [self._to_admin_schema(place) for place in self.repository.list()]

    def get_admin_place(self, place_id: str) -> PlaceAdminSchema | None:
        place = self.repository.get_by_id(place_id)
        if place is None:
            return None
        return self._to_admin_schema(place)

    def create_admin_place(self, payload: PlaceAdminSchema) -> PlaceAdminSchema:
        if self.repository.exists(payload.id):
            raise ValueError("Place already exists")

        place = Place(
            id=payload.id,
            title=payload.nome,
            details_title=payload.nome,
            description=payload.descrizione,
            cover_image_src=payload.immagine,
            cover_image_alt=payload.nome,
            event_date=None,
            address=payload.indirizzo,
            distance_km=payload.distanzaKm,
            category=payload.categoria,
            active=payload.attivo,
            sort_order=0,
        )
        place = self.repository.add(place)
        self.repository.replace_cover_image(place, payload.immagine, payload.nome)
        self.repository.update()
        return self._to_admin_schema(self.repository.get_by_id(place.id) or place)

    def update_admin_place(self, place_id: str, payload: PlaceAdminSchema) -> PlaceAdminSchema | None:
        place = self.repository.get_by_id(place_id)
        if place is None:
            return None

        place.title = payload.nome
        place.details_title = payload.nome
        place.description = payload.descrizione
        place.cover_image_src = payload.immagine
        place.cover_image_alt = payload.nome
        place.address = payload.indirizzo
        place.distance_km = payload.distanzaKm
        place.category = payload.categoria
        place.active = payload.attivo

        self.repository.replace_cover_image(place, payload.immagine, payload.nome)
        self.repository.update()
        return self._to_admin_schema(self.repository.get_by_id(place.id) or place)

    def delete_admin_place(self, place_id: str) -> bool:
        place = self.repository.get_by_id(place_id)
        if place is None:
            return False
        self.repository.delete(place)
        return True

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

    def _to_admin_schema(self, place: Place) -> PlaceAdminSchema:
        return PlaceAdminSchema(
            id=place.id,
            nome=place.title,
            descrizione=place.description,
            indirizzo=place.address or "",
            distanzaKm=float(place.distance_km) if place.distance_km is not None else 0,
            immagine=place.cover_image_src,
            categoria=place.category or "",
            attivo=place.active,
        )
