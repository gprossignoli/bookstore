from abc import ABC, abstractmethod

from src.application.command import Command


class CommandHandler(ABC):
	@abstractmethod
	def execute(self, command: Command) -> None:
		pass
