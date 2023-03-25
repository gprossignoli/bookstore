from dataclasses import dataclass

from bookstore.domain.event import Event


@dataclass(frozen=True)
class PurchaseCreatedEvent(Event):
	book_id: int
	quantity: int
	price: int
	user_id: str

	@classmethod
	def unique_identifier(cls) -> str:
		return "event.purchase.purchase_book.purchase_created"
