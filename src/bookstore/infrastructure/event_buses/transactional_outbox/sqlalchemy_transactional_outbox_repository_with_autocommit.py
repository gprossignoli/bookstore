from logging import Logger

from flask_sqlalchemy.session import Session

from bookstore.infrastructure.event_buses.transactional_outbox.outbox_record import (
    OutboxRecord,
)
from bookstore.infrastructure.event_buses.transactional_outbox.transactional_outbox_repository import (
    TransactionalOutboxRepository,
)


class SqlalchemyTransactionalOutboxRepositoryWithAutocommit(
    TransactionalOutboxRepository
):
    def __init__(self, db_session: Session):
        self.__db_session = db_session

    def save(self, record: OutboxRecord) -> None:
        try:
            self.__db_session.add(record)
            self.__db_session.commit()
        except Exception as e:
            self.__db_session.rollback()
            raise e

    def find(self, batch_size: int = 100):
        return list(
            OutboxRecord.query.filter(
                OutboxRecord.delivered_at == None,
                OutboxRecord.delivery_paused_at == None,
            )
            .order_by(OutboxRecord.created_at.asc())
            .limit(batch_size)
            .all()
        )
