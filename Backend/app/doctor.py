"""
Doctor class with real scheduling functionality.
Stage 2: Updated with appointment tracking.
"""
from typing import List, Tuple
from .identifiable import Identifiable
from .schedulable import Schedulable


class Doctor(Identifiable, Schedulable):
    """
    Represents a doctor in the hospital system.
    
    Attributes:
        name: Doctor's full name
        staff_id: Unique staff identifier
        specialty: Medical specialty
        _appointments: Scheduled appointments (private)
    """
    
    def __init__(self, name: str, staff_id: str, specialty: str):
        self.name = name
        self.staff_id = staff_id
        self.specialty = specialty
        self._appointments: List[Tuple[str, str]] = []
    
    def get_id(self) -> str:
        """Returns the unique staff ID."""
        return self.staff_id
    
    def is_available(self, date: str, time: str) -> bool:
        """Checks if doctor is available at specified date and time."""
        return (date, time) not in self._appointments
    
    def add_appointment(self, date: str, time: str) -> None:
        """Adds an appointment to doctor's schedule."""
        self._appointments.append((date, time))
    
    def remove_appointment(self, date: str, time: str) -> None:
        """Removes an appointment from doctor's schedule."""
        if (date, time) in self._appointments:
            self._appointments.remove((date, time))
    
    def __repr__(self):
        return f"<Doctor: Dr. {self.name} ({self.specialty})>"