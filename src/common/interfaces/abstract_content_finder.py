from abc import ABC, abstractmethod
from typing import Optional

from src.common.dto.content import ContentDTO


class AbstractContentFinder(ABC):

    @abstractmethod
    def find_content(self, url: str, headers: dict, cookies: Optional[dict] = None) -> list[ContentDTO]:
        raise NotImplementedError
