from abc import ABC, abstractmethod

from src.common.dto.content import ContentDTO
from src.common.types import PathToContent


class AbstractContentDownloader(ABC):
    @abstractmethod
    def download_content(self, content: list[ContentDTO]) -> list[PathToContent]:
        pass
