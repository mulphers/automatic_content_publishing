from typing import Generator

from odmantic import SyncEngine

from src.database.core.gateway import DatabaseGateway, database_gateway_factory
from src.database.core.unit_of_work import (OdmanticUnitOfWork,
                                            unit_of_work_factory)

__all__ = (
    'DatabaseGateway',
    'TransactionGateway',
    'OdmanticUnitOfWork',
    'database_gateway_factory',
    'unit_of_work_factory',
)


class TransactionGateway:
    def __init__(self, engine: SyncEngine) -> None:
        self.engine = engine

    def __call__(self) -> Generator[DatabaseGateway, None, None]:
        with database_gateway_factory(uow=unit_of_work_factory(self.engine.session())) as gateway:
            yield gateway
