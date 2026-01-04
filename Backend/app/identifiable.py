from abc import ABC, abstractmethod

class Identifiable(ABC):
    """
    Enforces every entity to have a unique identifier.
    """
    @abstractmethod
    def get_id(self) -> str:
        pass