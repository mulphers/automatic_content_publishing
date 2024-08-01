from abc import ABC, abstractmethod
from typing import Optional

from src.common.dto.content import ContentDTO


class AbstractContentFinder(ABC):

    @property
    @abstractmethod
    def _host(self) -> str:
        """
        This is a class attribute.

        Usage:

            class MyContentFinder(AbstractContentFinder):
                _host = 'your_host'

                ...
        """

        raise NotImplementedError

    @abstractmethod
    def find_content(self, headers: dict, cookies: Optional[dict] = None) -> list[ContentDTO]:
        raise NotImplementedError
