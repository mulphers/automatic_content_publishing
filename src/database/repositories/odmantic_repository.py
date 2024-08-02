from typing import Any, Optional, Sequence

from odmantic.engine import ModelType
from odmantic.session import SyncSession

from src.common.interfaces.abstract_repository import AbstractRepository


class OdmanticRepository(AbstractRepository[ModelType, SyncSession, bool]):
    def create(self, data: dict[str, Any]) -> Optional[ModelType]:
        return self.session.save(self.model(**data))

    def select(self, *clauses: bool) -> Optional[ModelType]:
        return self.session.find_one(self.model, *clauses)

    def select_many(
            self,
            *clauses: bool,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Sequence[ModelType]:
        return tuple(self.session.find(self.model, *clauses))

    def update(self, *clauses: bool, data: dict[str, Any]) -> Optional[ModelType]:
        instance = self.select(*clauses)

        if instance:
            for key, value in data.items():
                setattr(instance, key, value)

            return self.session.save(instance)

        return None

    def delete(self, *clauses: bool) -> Sequence[ModelType]:
        removed_users = self.select_many(*clauses)
        self.session.remove(self.model, *clauses)

        return removed_users
