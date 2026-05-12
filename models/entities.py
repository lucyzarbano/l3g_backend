from __future__ import annotations

from typing import Optional

from sqlalchemy import Boolean, DECIMAL, BigInteger, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text)
    short_description: Mapped[str] = mapped_column(String(500))
    cover_image_src: Mapped[str] = mapped_column(String(500))
    cover_image_alt: Mapped[str] = mapped_column(String(255))
    link: Mapped[str] = mapped_column(String(255))
    rate: Mapped[float] = mapped_column(DECIMAL(2, 1), default=0)
    price_base: Mapped[Optional[float]] = mapped_column(DECIMAL(8, 2), nullable=True)
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    visible_in_home: Mapped[bool] = mapped_column(Boolean, default=True)
    reverse_layout: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    images: Mapped[list["RoomImage"]] = relationship(back_populates="room", cascade="all, delete-orphan")
    badges: Mapped[list["RoomBadge"]] = relationship(back_populates="room", cascade="all, delete-orphan")
    room_services: Mapped[list["RoomService"]] = relationship(back_populates="room", cascade="all, delete-orphan")


class RoomImage(Base):
    __tablename__ = "room_images"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    room_id: Mapped[str] = mapped_column(ForeignKey("rooms.id"))
    src: Mapped[str] = mapped_column(String(500))
    alt: Mapped[str] = mapped_column(String(255))
    is_cover: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    room: Mapped[Room] = relationship(back_populates="images")


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    icon_key: Mapped[str] = mapped_column(String(120))


class RoomService(Base):
    __tablename__ = "room_services"

    room_id: Mapped[str] = mapped_column(ForeignKey("rooms.id"), primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), primary_key=True)
    service_group: Mapped[str] = mapped_column(Enum("base", "additional"), primary_key=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    room: Mapped[Room] = relationship(back_populates="room_services")
    service: Mapped[Service] = relationship()


class RoomBadge(Base):
    __tablename__ = "room_badges"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    room_id: Mapped[str] = mapped_column(ForeignKey("rooms.id"))
    label: Mapped[str] = mapped_column(String(120))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    room: Mapped[Room] = relationship(back_populates="badges")


class Place(Base):
    __tablename__ = "places"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(160))
    details_title: Mapped[str] = mapped_column(String(220))
    description: Mapped[str] = mapped_column(Text)
    cover_image_src: Mapped[str] = mapped_column(String(500))
    cover_image_alt: Mapped[str] = mapped_column(String(255))
    event_date: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    distance_km: Mapped[Optional[float]] = mapped_column(DECIMAL(6, 2), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    images: Mapped[list["PlaceImage"]] = relationship(back_populates="place")
    info_items: Mapped[list["PlaceInfoItem"]] = relationship(back_populates="place")


class PlaceImage(Base):
    __tablename__ = "place_images"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    place_id: Mapped[str] = mapped_column(ForeignKey("places.id"))
    src: Mapped[str] = mapped_column(String(500))
    alt: Mapped[str] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    place: Mapped[Place] = relationship(back_populates="images")


class PlaceInfoItem(Base):
    __tablename__ = "place_info_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    place_id: Mapped[str] = mapped_column(ForeignKey("places.id"))
    icon_key: Mapped[str] = mapped_column(String(120))
    title: Mapped[str] = mapped_column(String(160))
    type: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    place: Mapped[Place] = relationship(back_populates="info_items")


class AboutSection(Base):
    __tablename__ = "about_sections"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    eyebrow: Mapped[str] = mapped_column(String(160))
    title: Mapped[str] = mapped_column(String(160))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    paragraphs: Mapped[list["AboutParagraph"]] = relationship(back_populates="section")
    images: Mapped[list["AboutImage"]] = relationship(back_populates="section")


class AboutParagraph(Base):
    __tablename__ = "about_paragraphs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    about_section_id: Mapped[str] = mapped_column(ForeignKey("about_sections.id"))
    body: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    section: Mapped[AboutSection] = relationship(back_populates="paragraphs")


class AboutImage(Base):
    __tablename__ = "about_images"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    about_section_id: Mapped[str] = mapped_column(ForeignKey("about_sections.id"))
    src: Mapped[str] = mapped_column(String(500))
    alt: Mapped[str] = mapped_column(String(255))
    class_name: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    section: Mapped[AboutSection] = relationship(back_populates="images")
