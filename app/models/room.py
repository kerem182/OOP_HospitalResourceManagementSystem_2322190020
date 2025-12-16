from .identifiable import Identifiable
from .schedulable import Schedulable

class Room(Identifiable, Schedulable):
    """
    Represents a hospital room.
    """
    def __init__(self, room_number: int, capacity: int, type: str):
        self.room_number = room_number
        self.capacity = capacity
        self.type = type

    def get_id(self) -> str:
        return str(self.room_number)

    def is_available(self, date: str, time: str) -> bool:
        return True

    def __repr__(self):
        return f"<Room: {self.room_number} ({self.type})>"