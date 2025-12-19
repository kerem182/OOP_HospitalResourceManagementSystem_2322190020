"""
Room class representing hospital rooms.
Stage 2: Added appointment tracking for real availability checks.
"""
from typing import List, Tuple
from .identifiable import Identifiable
from .schedulable import Schedulable


class Room(Identifiable, Schedulable):
    """Represents a hospital room."""
    
    def __init__(self, room_number: int, capacity: int, room_type: str):
        self.room_number = room_number
        self.capacity = capacity
        self.type = room_type
        self._appointments: List[Tuple[str, str]] = [] # Resource schedule list
    
    def get_id(self) -> str:
        """Returns room number as string."""
        return str(self.room_number)
    
    def is_available(self, date: str, time: str) -> bool:
        """Checks if room is available at specified date and time."""
        return (date, time) not in self._appointments
    
    def add_appointment(self, date: str, time: str) -> None:
        """Adds an appointment to room's schedule."""
        self._appointments.append((date, time))
    
    def remove_appointment(self, date: str, time: str) -> None:
        """Removes an appointment from room's schedule."""
        if (date, time) in self._appointments:
            self._appointments.remove((date, time))
    
    def __repr__(self):
        return f"<Room: {self.room_number} ({self.type})>"