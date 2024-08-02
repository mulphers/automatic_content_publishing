from typing import Optional, Sequence, Type

from src.common.dto.content import ContentCreate, ContentUpdate
from src.database.models.content import Content
from src.database.repositories.odmantic_repository import OdmanticRepository


class ContentRepository(OdmanticRepository[Content]):
    model: Type[Content] = Content

    def create_content(self, content: ContentCreate) -> Optional[Content]:
        return self.create(data=content.model_dump(exclude_none=True))

    def find_all_content(self) -> Sequence[Content]:
        return self.select_many()

    def read_content_by_content_id(self, content_id: int) -> Optional[Content]:
        return self.select(self.model.content_id == content_id)

    def update_content_by_content_id(self, content_id: int, content: ContentUpdate) -> Optional[Content]:
        return self.update(self.model.content_id == content_id, data=content.model_dump(exclude_none=True))

    def delete_content_by_content_id(self, content_id: int) -> Sequence[Content]:
        return self.delete(self.model.content_id == content_id)
