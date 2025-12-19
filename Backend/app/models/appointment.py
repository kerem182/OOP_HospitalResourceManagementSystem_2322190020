"""
Appointment class demonstrating composition.
Stage 2: Added status management and Room composition.
"""
from .identifiable import Identifiable
from .patient import Patient
from .doctor import Doctor
from .room import Room # Room object imported


class Appointment(Identifiable):
    """
    Represents a medical appointment.
    Demonstrates composition: contains Patient, Doctor, and Room objects.
    """
    
    def __init__(self, date: str, time: str, reason: str, 
                 patient: Patient, doctor: Doctor, room: Room): # Added room
        self.date = date
        self.time = time
        self.reason = reason
        self.patient = patient 
        self.doctor = doctor 
        self.room = room # Composition
        self.status = "scheduled"
    
    def get_id(self) -> str:
        """Returns unique appointment identifier."""
        return f"{self.date}_{self.time}_{self.patient.get_id()}_{self.room.get_id()}" # Room ID added for better uniqueness
    
    def cancel(self) -> None:
        """Marks appointment as cancelled."""
        self.status = "cancelled"
    
    def __repr__(self):
        return (f"<Appointment: {self.date} at {self.time} - "
                f"Dr. {self.doctor.name} in Room {self.room.room_number}>")