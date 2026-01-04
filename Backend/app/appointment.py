"""
Appointment class demonstrating composition.
Stage 3: Added room reference for complete tracking.
"""
from .identifiable import Identifiable
from .patient import Patient
from .doctor import Doctor
from .room import Room


class Appointment(Identifiable):
    """
    Represents a medical appointment.
    Demonstrates composition: contains Patient, Doctor, and Room objects.
    """
    
    def __init__(self, date: str, time: str, reason: str, 
                 patient: Patient, doctor: Doctor, room: Room):
        self.date = date
        self.time = time
        self.reason = reason
        self.patient = patient  # Composition
        self.doctor = doctor    # Composition
        self.room = room        # Composition
        self.status = "scheduled"
    
    def get_id(self) -> str:
        """Returns unique appointment identifier."""
        return f"{self.date}_{self.time}_{self.patient.get_id()}"
    
    def cancel(self) -> None:
        """Marks appointment as cancelled."""
        self.status = "cancelled"
    
    def __repr__(self):
        return (f"<Appointment: {self.date} at {self.time} - "
                f"{self.doctor.specialty} ({self.patient.name}) "
                f"in Room {self.room.room_number}>")