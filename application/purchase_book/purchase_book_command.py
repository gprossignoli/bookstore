from application.command import Command


class PurchaseBookCommand(Command):
	def __init__(self, book_id: int, user_id: str, quantity: int):
		self.__book_id = book_id
		self.__user_id = user_id
		self.__quantity = quantity

	def execute(self) -> None:
		return
