from src.common.dto.content import ContentCreate, ContentDTO
from src.common.interfaces.abstract_content_unique_checker import \
    AbstractContentUniqueChecker
from src.database import DatabaseGateway


class ContentUniqueCheckerWithDatabase(AbstractContentUniqueChecker):
    def drop_pending_content(self, gateway: DatabaseGateway, content: list[ContentDTO]) -> int:
        return len(self.find_new_content(gateway=gateway, content=content))

    def find_new_content(self, gateway: DatabaseGateway, content: list[ContentDTO]) -> list[ContentDTO]:
        content_repository = gateway.content_repository()

        old_content_id = tuple(map(lambda item: item.content_id, content_repository.find_all_content()))
        new_content = list(filter(lambda item: item.content_id not in old_content_id, content))

        for obj in new_content:
            content_repository.create_content(content=ContentCreate(**obj.model_dump()))

        return new_content
