"""
Room class representing hospital rooms.
Stage 3: Added reservation tracking for appointment scheduling.
"""
from typing import List, Tuple
from .identifiable import Identifiable
from .schedulable import Schedulable


class Room(Identifiable, Schedulable):
    """
    Represents a hospital room.
    
    Attributes:
        room_number: Unique room identifier
        capacity: Maximum occupancy
        type: Room type (e.g., Surgery Room, ICU, Standard)
        _reservations: List of scheduled reservations (date, time tuples)
    """
    
    def __init__(self, room_number: int, capacity: int, room_type: str):
        self.room_number = room_number
        self.capacity = capacity
        self.type = room_type
        self._reservations: List[Tuple[str, str]] = []  # [(date, time), ...]
    
    def get_id(self) -> str:
        """Returns room number as string."""
        return str(self.room_number)
    
    def is_available(self, date: str, time: str) -> bool:
        """
        Checks if the room is available at the specified date and time.
        
        Args:
            date: Reservation date (format: YYYY-MM-DD)
            time: Reservation time (format: HH:MM)
            
        Returns:
            True if available, False otherwise
        """
        return (date, time) not in self._reservations
    
    def add_reservation(self, date: str, time: str) -> None:
        """
        Adds a reservation to the room's schedule.
        
        Args:
            date: Reservation date
            time: Reservation time
        """
        if not self.is_available(date, time):
            from .exceptions import AppointmentConflictError
            raise AppointmentConflictError(date, time, f"Room {self.room_number}")
        self._reservations.append((date, time))
    
    def remove_reservation(self, date: str, time: str) -> None:
        """
        Removes a reservation from the room's schedule.
        
        Args:
            date: Reservation date
            time: Reservation time
        """
        if (date, time) in self._reservations:
            self._reservations.remove((date, time))
    
    def get_reservations(self) -> List[Tuple[str, str]]:
        """Returns a copy of the room's reservation schedule."""
        return self._reservations.copy()
    
    def __repr__(self):
        return f"<Room: {self.room_number} ({self.type})>"