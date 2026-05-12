from __future__ import annotations

from models.schemas import AboutImageSchema, AboutSchema
from repository.about_repository import AboutRepository


class AboutService:
    def __init__(self, repository: AboutRepository) -> None:
        self.repository = repository

    def get_about(self) -> AboutSchema | None:
        section = self.repository.get_active()
        if section is None:
            return None

        return AboutSchema(
            id=section.id,
            eyebrow=section.eyebrow,
            title=section.title,
            description=[
                paragraph.body
                for paragraph in sorted(section.paragraphs, key=lambda item: item.sort_order)
            ],
            images=[
                AboutImageSchema(src=image.src, alt=image.alt, class_name=image.class_name)
                for image in sorted(section.images, key=lambda item: item.sort_order)
            ],
        )
