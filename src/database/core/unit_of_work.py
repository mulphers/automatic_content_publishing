from odmantic.session import SyncSession, SyncTransaction

from src.common.interfaces.abstract_unit_of_work import AbstractUnitOfWork


class OdmanticUnitOfWork(AbstractUnitOfWork[SyncSession, SyncTransaction]):
    def commit(self) -> None:
        if self.transaction:
            self.transaction.commit()

    def rollback(self) -> None:
        if self.transaction:
            self.transaction.abort()

    def create_transaction(self) -> None:
        self.session.start()
        self.transaction = self.session.transaction()
        self.transaction.start()

    def close_transaction(self) -> None:
        if self.transaction:
            self.transaction.__exit__(None, None, None)
            self.transaction = None
            self.session.end()


def unit_of_work_factory(session: SyncSession) -> OdmanticUnitOfWork:
    return OdmanticUnitOfWork(session=session)
