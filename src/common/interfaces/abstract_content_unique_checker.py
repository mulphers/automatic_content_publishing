from abc import ABC, abstractmethod

from src.common.dto.content import ContentDTO
from src.database import DatabaseGateway


class AbstractContentUniqueChecker(ABC):
    @abstractmethod
    def drop_pending_content(self, gateway: DatabaseGateway, content: list[ContentDTO]) -> int:
        pass

    @abstractmethod
    def find_new_content(self, gateway: DatabaseGateway, content: list[ContentDTO]) -> list[ContentDTO]:
        pass
