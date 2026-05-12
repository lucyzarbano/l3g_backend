from __future__ import annotations

from models.entities import Room
from models.schemas import ImageSchema, RoomAdminSchema, RoomSchema, ServiceSchema
from repository.room_repository import RoomRepository


class RoomService:
    def __init__(self, repository: RoomRepository) -> None:
        self.repository = repository

    def list_rooms(self) -> list[RoomSchema]:
        return [self._to_schema(room) for room in self.repository.list()]

    def get_room(self, room_id: str) -> RoomSchema | None:
        room = self.repository.get_by_id(room_id)
        if room is None:
            return None
        return self._to_schema(room)

    def list_admin_rooms(self) -> list[RoomAdminSchema]:
        return [self._to_admin_schema(room) for room in self.repository.list()]

    def get_admin_room(self, room_id: str) -> RoomAdminSchema | None:
        room = self.repository.get_by_id(room_id)
        if room is None:
            return None
        return self._to_admin_schema(room)

    def create_admin_room(self, payload: RoomAdminSchema) -> RoomAdminSchema:
        if self.repository.exists(payload.id):
            raise ValueError("Room already exists")

        room = Room(
            id=payload.id,
            title=payload.nome,
            description=payload.descrizione,
            short_description=self._short_description(payload.descrizione),
            cover_image_src=payload.immagineCopertina,
            cover_image_alt=payload.nome,
            link=f"/room/{payload.id}",
            rate=0,
            price_base=payload.prezzoBase,
            capacity=payload.capienza,
            visible_in_home=True,
            reverse_layout=False,
            active=payload.attiva,
            sort_order=0)
        room = self.repository.add(room)
        self.repository.replace_cover_image(room, payload.immagineCopertina, payload.nome)
        self.repository.replace_base_services(room, self._clean_services(payload.servizi))
        self.repository.update()
        return self._to_admin_schema(self.repository.get_by_id(room.id) or room)

    def update_admin_room(self, room_id: str, payload: RoomAdminSchema) -> RoomAdminSchema | None:
        room = self.repository.get_by_id(room_id)
        if room is None:
            return None

        room.title = payload.nome
        room.description = payload.descrizione
        room.short_description = self._short_description(payload.descrizione)
        room.cover_image_src = payload.immagineCopertina
        room.cover_image_alt = payload.nome
        room.price_base = payload.prezzoBase
        room.capacity = payload.capienza
        room.active = payload.attiva

        self.repository.replace_cover_image(room, payload.immagineCopertina, payload.nome)
        self.repository.replace_base_services(room, self._clean_services(payload.servizi))
        self.repository.update()
        return self._to_admin_schema(self.repository.get_by_id(room.id) or room)

    def delete_admin_room(self, room_id: str) -> bool:
        room = self.repository.get_by_id(room_id)
        if room is None:
            return False
        self.repository.delete(room)
        return True

    def _to_schema(self, room: Room) -> RoomSchema:
        services_base = []
        services_additional = []
        for room_service in sorted(room.room_services, key=lambda item: item.sort_order):
            service = ServiceSchema(
                description=room_service.service.name,
                icon_key=room_service.service.icon_key,
            )
            if room_service.service_group == "additional":
                services_additional.append(service)
            else:
                services_base.append(service)

        return RoomSchema(
            id=room.id,
            title=room.title,
            description=room.description,
            short_description=room.short_description,
            cover_image=ImageSchema(src=room.cover_image_src, alt=room.cover_image_alt),
            link=room.link,
            rate=float(room.rate),
            price_base=float(room.price_base) if room.price_base is not None else None,
            capacity=room.capacity,
            visible_in_home=room.visible_in_home,
            reverse_layout=room.reverse_layout,
            active=room.active,
            images=[
                ImageSchema(src=image.src, alt=image.alt)
                for image in sorted(room.images, key=lambda item: item.sort_order)
            ],
            services_base=services_base,
            services_additional=services_additional,
            badges=[badge.label for badge in sorted(room.badges, key=lambda item: item.sort_order)],
        )

    def _to_admin_schema(self, room: Room) -> RoomAdminSchema:
        services = [
            room_service.service.name
            for room_service in sorted(room.room_services, key=lambda item: item.sort_order)
            if room_service.service_group == "base"
        ]

        return RoomAdminSchema(
            id=room.id,
            nome=room.title,
            descrizione=room.description,
            prezzoBase=float(room.price_base) if room.price_base is not None else 0,
            capienza=room.capacity or 1,
            immagineCopertina=room.cover_image_src,
            servizi=services,
            attiva=room.active,
        )

    def _short_description(self, description: str) -> str:
        clean_description = " ".join(description.split())
        return clean_description[:497] + "..." if len(clean_description) > 500 else clean_description

    def _clean_services(self, services: list[str]) -> list[str]:
        unique_services = []
        for service in services:
            clean_service = service.strip()
            if clean_service and clean_service not in unique_services:
                unique_services.append(clean_service)
        return unique_services
