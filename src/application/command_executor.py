from src.application.command import Command
from src.application.purchase_book.purchase_book_command import PurchaseBookCommand
from src.application.purchase_book.purchase_book_command_handler import PurchaseBookCommandHandler


class CommandExecutor:
	__mapper = {
		PurchaseBookCommand.fqn(): PurchaseBookCommandHandler.execute
	}

	def execute(self, command: Command) -> None:
		self.__mapper.get(command.fqn()).__call__(command=command)
# este call necesita implementacion en la clase creo.