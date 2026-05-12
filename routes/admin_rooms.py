from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from lib.auth import get_current_admin_user
from lib.db_session import get_db
from models.schemas import RoomAdminSchema
from repository.room_repository import RoomRepository
from services.room_service import RoomService

router = APIRouter(dependencies=[Depends(get_current_admin_user)])


def get_room_service(db: Session = Depends(get_db)) -> RoomService:
    return RoomService(RoomRepository(db))


@router.get("", response_model=list[RoomAdminSchema])
def list_admin_rooms(service: RoomService = Depends(get_room_service)) -> list[RoomAdminSchema]:
    return service.list_admin_rooms()


@router.get("/{room_id}", response_model=RoomAdminSchema)
def get_admin_room(room_id: str, service: RoomService = Depends(get_room_service)) -> RoomAdminSchema:
    room = service.get_admin_room(room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.post("", response_model=RoomAdminSchema, status_code=status.HTTP_201_CREATED)
def create_admin_room(
    payload: RoomAdminSchema,
    service: RoomService = Depends(get_room_service),
) -> RoomAdminSchema:
    try:
        return service.create_admin_room(payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.put("/{room_id}", response_model=RoomAdminSchema)
def update_admin_room(
    room_id: str,
    payload: RoomAdminSchema,
    service: RoomService = Depends(get_room_service),
) -> RoomAdminSchema:
    room = service.update_admin_room(room_id, payload)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin_room(room_id: str, service: RoomService = Depends(get_room_service)) -> Response:
    deleted = service.delete_admin_room(room_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Room not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
