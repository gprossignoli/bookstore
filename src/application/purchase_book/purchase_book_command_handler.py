from src.application.command_handler import CommandHandler
from src.application.purchase_book.purchase_book_command import PurchaseBookCommand


"""
generar un modelo purchase con los datos del command, añadiendo created_at
guardar en db el purchase
crear el evento purchase_created
publicar el evento
"""


class PurchaseBookCommandHandler(CommandHandler):
	def execute(self, command: PurchaseBookCommand) -> None:
		print("executing command handler")
