from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Generic, Optional, Type

from src.common.types import SessionType, TransactionType


class AbstractUnitOfWork(ABC, Generic[SessionType, TransactionType]):
    def __init__(self, session: SessionType) -> None:
        self.session = session
        self.transaction: Optional[TransactionType] = None

    def __enter__(self) -> AbstractUnitOfWork:
        self.create_transaction()
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()

        self.close_transaction()

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_transaction(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close_transaction(self) -> None:
        raise NotImplementedError
