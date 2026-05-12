from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class ReadRepository(ABC, Generic[T]):
    @abstractmethod
    def list(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, item_id: str) -> T | None:
        raise NotImplementedError
