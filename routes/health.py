from fastapi import APIRouter
from sqlalchemy import text

from lib.database import engine

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, bool]:
    return {"ok": True}


@router.get("/health/db")
def database_health_check() -> dict[str, bool | int]:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1")).scalar_one()
    return {"ok": True, "db": result}
