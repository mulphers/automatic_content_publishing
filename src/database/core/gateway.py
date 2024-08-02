from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

from src.common.interfaces.abstract_unit_of_work import AbstractUnitOfWork
from src.database.repositories.content_repository import ContentRepository


class DatabaseGateway:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    def __enter__(self) -> DatabaseGateway:
        self.uow.__enter__()
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> None:
        self.uow.__exit__(exc_type, exc_val, exc_tb)

    def content_repository(self) -> ContentRepository:
        return ContentRepository(self.uow.session)


def database_gateway_factory(uow: AbstractUnitOfWork) -> DatabaseGateway:
    return DatabaseGateway(uow=uow)
