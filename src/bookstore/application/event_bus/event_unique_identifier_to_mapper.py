from bookstore.domain.event import Event
from bookstore.domain.purchase_book import PurchaseCreatedEvent


class EventUniqueIdentifierToMapper:
    __mapper = {
        PurchaseCreatedEvent.unique_identifier(): PurchaseCreatedEvent
    }

    @classmethod
    def get_event(cls, unique_identifier: str) -> Event:
        return cls.__mapper[unique_identifier]
