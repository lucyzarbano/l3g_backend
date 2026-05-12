from __future__ import annotations

from sqlalchemy.orm import Session, selectinload

from abstractrepository.base_repository import ReadRepository
from models.entities import Room, RoomImage, RoomService, Service


class RoomRepository(ReadRepository[Room]):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> list[Room]:
        return (
            self.db.query(Room)
            .options(
                selectinload(Room.images),
                selectinload(Room.badges),
                selectinload(Room.room_services).selectinload(RoomService.service),
            )
            .order_by(Room.sort_order, Room.title)
            .all()
        )

    def get_by_id(self, item_id: str) -> Room | None:
        return (
            self.db.query(Room)
            .options(
                selectinload(Room.images),
                selectinload(Room.badges),
                selectinload(Room.room_services).selectinload(RoomService.service),
            )
            .filter(Room.id == item_id)
            .first()
        )

    def exists(self, item_id: str) -> bool:
        return self.db.query(Room.id).filter(Room.id == item_id).first() is not None

    def add(self, room: Room) -> Room:
        self.db.add(room)
        self.db.commit()
        return self.get_by_id(room.id) or room

    def update(self) -> None:
        self.db.commit()

    def delete(self, room: Room) -> None:
        self.db.delete(room)
        self.db.commit()

    def get_or_create_service(self, name: str) -> Service:
        service = self.db.query(Service).filter(Service.name == name).first()
        if service is not None:
            return service

        service = Service(name=name, icon_key=self._guess_icon_key(name))
        self.db.add(service)
        self.db.flush()
        return service

    def replace_cover_image(self, room: Room, src: str, alt: str) -> None:
        cover = next((image for image in room.images if image.is_cover), None)
        if cover is None:
            cover = RoomImage(room_id=room.id, src=src, alt=alt, is_cover=True, sort_order=1)
            self.db.add(cover)
        else:
            cover.src = src
            cover.alt = alt

    def replace_base_services(self, room: Room, service_names: list[str]) -> None:
        for room_service in list(room.room_services):
            if room_service.service_group == "base":
                self.db.delete(room_service)
        self.db.flush()

        for index, service_name in enumerate(service_names, start=1):
            service = self.get_or_create_service(service_name)
            self.db.add(
                RoomService(
                    room_id=room.id,
                    service_id=service.id,
                    service_group="base",
                    sort_order=index,
                )
            )

    def _guess_icon_key(self, service_name: str) -> str:
        value = service_name.lower()
        if "wifi" in value:
            return "faWifi"
        if "bagno" in value:
            return "faSink"
        if "balcone" in value:
            return "faLocationDot"
        if "aria" in value or "clima" in value:
            return "faTemperatureArrowDown"
        if "tv" in value:
            return "faTv"
        if "parcheggio" in value:
            return "faSquareParking"
        if "vista" in value or "citta" in value:
            return "faCity"
        return "faTag"
