from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from lib.db_session import get_db
from models.schemas import RoomSchema
from repository.room_repository import RoomRepository
from services.room_service import RoomService

router = APIRouter()


def get_room_service(db: Session = Depends(get_db)) -> RoomService:
    return RoomService(RoomRepository(db))


@router.get("", response_model=list[RoomSchema])
def list_rooms(service: RoomService = Depends(get_room_service)) -> list[RoomSchema]:
    return service.list_rooms()


@router.get("/{room_id}", response_model=RoomSchema)
def get_room(room_id: str, service: RoomService = Depends(get_room_service)) -> RoomSchema:
    room = service.get_room(room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


