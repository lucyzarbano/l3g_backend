from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from lib.db_session import get_db
from models.schemas import PlaceSchema
from repository.place_repository import PlaceRepository
from services.place_service import PlaceService

router = APIRouter()


def get_place_service(db: Session = Depends(get_db)) -> PlaceService:
    return PlaceService(PlaceRepository(db))


@router.get("", response_model=list[PlaceSchema])
def list_places(service: PlaceService = Depends(get_place_service)) -> list[PlaceSchema]:
    return service.list_places()


@router.get("/{place_id}", response_model=PlaceSchema)
def get_place(place_id: str, service: PlaceService = Depends(get_place_service)) -> PlaceSchema:
    place = service.get_place(place_id)
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return place
