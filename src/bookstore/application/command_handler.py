from abc import ABC, abstractmethod

from bookstore.application.command import Command


class CommandHandler(ABC):
    @abstractmethod
    def execute(self, command: Command) -> None:
        pass
