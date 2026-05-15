from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from lib.auth import get_current_admin_user
from lib.db_session import get_db
from models.schemas import PlaceAdminSchema
from repository.place_repository import PlaceRepository
from services.place_service import PlaceService

router = APIRouter(dependencies=[Depends(get_current_admin_user)])


def get_place_service(db: Session = Depends(get_db)) -> PlaceService:
    return PlaceService(PlaceRepository(db))


@router.get("", response_model=list[PlaceAdminSchema])
def list_admin_places(service: PlaceService = Depends(get_place_service)) -> list[PlaceAdminSchema]:
    return service.list_admin_places()


@router.get("/{place_id}", response_model=PlaceAdminSchema)
def get_admin_place(place_id: str, service: PlaceService = Depends(get_place_service)) -> PlaceAdminSchema:
    place = service.get_admin_place(place_id)
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.post("", response_model=PlaceAdminSchema, status_code=status.HTTP_201_CREATED)
def create_admin_place(
    payload: PlaceAdminSchema,
    service: PlaceService = Depends(get_place_service),
) -> PlaceAdminSchema:
    try:
        return service.create_admin_place(payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.put("/{place_id}", response_model=PlaceAdminSchema)
def update_admin_place(
    place_id: str,
    payload: PlaceAdminSchema,
    service: PlaceService = Depends(get_place_service),
) -> PlaceAdminSchema:
    place = service.update_admin_place(place_id, payload)
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin_place(place_id: str, service: PlaceService = Depends(get_place_service)) -> Response:
    deleted = service.delete_admin_place(place_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Place not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

