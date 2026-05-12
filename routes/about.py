from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from lib.db_session import get_db
from models.schemas import AboutSchema
from repository.about_repository import AboutRepository
from services.about_service import AboutService

router = APIRouter()


def get_about_service(db: Session = Depends(get_db)) -> AboutService:
    return AboutService(AboutRepository(db))


@router.get("", response_model=AboutSchema)
def get_about(service: AboutService = Depends(get_about_service)) -> AboutSchema:
    about = service.get_about()
    if about is None:
        raise HTTPException(status_code=404, detail="About section not found")
    return about
