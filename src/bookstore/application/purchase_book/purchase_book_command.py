from dataclasses import dataclass

from bookstore.application.command import Command


"""
Para mañana, esta clase pasa a ser dataclass, se crea un command_executer o algo asi que tenga mappeo interno de los comandos,
el command handler recibe el comando e implementar commandhandler.
"""


@dataclass()
class PurchaseBookCommand(Command):
	book_id: int
	user_id: str
	quantity: int

	@classmethod
	def fqn(cls) -> str:
		return "command.purchase_book"
