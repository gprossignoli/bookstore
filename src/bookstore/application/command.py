from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Command(ABC):
    @abstractmethod
    def fqn(self) -> str:
        return NotImplemented
