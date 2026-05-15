from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lib.config import settings
from lib.logger import configure_logger, get_logger
from routes import about, admin_places, admin_rooms, auth, health, places, rooms

configure_logger()
logger = get_logger(__name__)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(admin_rooms.router, prefix="/api/admin/rooms", tags=["admin rooms"])
app.include_router(admin_places.router, prefix="/api/admin/places", tags=["admin places"])
app.include_router(rooms.router, prefix="/api/rooms", tags=["rooms"])
app.include_router(places.router, prefix="/api/places", tags=["places"])
app.include_router(about.router, prefix="/api/about", tags=["about"])


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Starting %s on %s:%s", settings.app_name, settings.api_host, settings.api_port)


@app.on_event("shutdown")
def on_shutdown() -> None:
    logger.info("Shutting down %s", settings.app_name)
