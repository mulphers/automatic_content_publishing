from abc import ABC, abstractmethod

from src.common.types import PathToContent


class AbstractContentPublisher(ABC):
    @abstractmethod
    def publish_content(self, paths: list[PathToContent]) -> None:
        pass
