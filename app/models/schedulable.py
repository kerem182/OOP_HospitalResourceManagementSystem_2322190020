from abc import ABC, abstractmethod

class Schedulable(ABC):
    """
    Interface for availability checking.
    """
    @abstractmethod
    def is_available(self, date: str, time: str) -> bool:
        pass