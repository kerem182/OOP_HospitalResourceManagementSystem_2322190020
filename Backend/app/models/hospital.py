"""
Hospital coordinator class - manages all resources.
Stage 2: Core functionality with Dependency Injection (Room integration added).
"""
from typing import Dict, List, Optional
from .patient import Patient
from .doctor import Doctor
from .room import Room 
from .appointment import Appointment
from .exceptions import (
    PatientNotFoundError,
    DoctorNotFoundError,
    RoomNotFoundError, # New
    AppointmentConflictError,
    InvalidAppointmentError
)


class Hospital:
    """
    Central coordinator for hospital resource management.
    Uses dependency injection to manage associations.
    """
    
    def __init__(self, name: str):
        self.name = name
        self._patients: Dict[str, Patient] = {}
        self._doctors: Dict[str, Doctor] = {}
        self._rooms: Dict[str, Room] = {} # Dictionary to store room objects
        self._appointments: Dict[str, Appointment] = {}
    
    # ==================== REGISTRATION ====================
    
    def register_patient(self, patient: Patient) -> None:
        """Registers a patient in the system."""
        self._patients[patient.get_id()] = patient
    
    def register_doctor(self, doctor: Doctor) -> None:
        """Registers a doctor in the system."""
        self._doctors[doctor.get_id()] = doctor
    
    def register_room(self, room: Room) -> None: 
        """Registers a room in the system."""
        self._rooms[room.get_id()] = room
    
    # ==================== SEARCH ALGORITHMS ====================
    
    def find_patient_by_id(self, patient_id: str) -> Optional[Patient]:
        """Finds patient by ID."""
        return self._patients.get(patient_id)
    
    def find_doctor_by_id(self, doctor_id: str) -> Optional[Doctor]:
        """Finds doctor by ID."""
        return self._doctors.get(doctor_id)

    def find_room_by_id(self, room_id: str) -> Optional[Room]: 
        """Finds room by ID."""
        return self._rooms.get(room_id)
    
    def find_doctor_by_specialty(self, specialty: str) -> List[Doctor]:
        """Finds all doctors with given specialty."""
        specialty_lower = specialty.lower()
        return [
            d for d in self._doctors.values()
            if specialty_lower in d.specialty.lower()
        ]
    
    # ==================== APPOINTMENT SCHEDULING ====================
    
    def schedule_appointment(
        self,
        patient_id: str,
        doctor_id: str,
        room_id: str, # Added room_id parameter
        date: str,
        time: str,
        reason: str
    ) -> Appointment:
        """
        Schedules a new appointment. Checks doctor AND room availability.
        
        Raises:
            PatientNotFoundError: Patient doesn't exist
            DoctorNotFoundError: Doctor doesn't exist
            RoomNotFoundError: Room doesn't exist
            AppointmentConflictError: Time slot not available
            InvalidAppointmentError: Invalid data
        """
        # Validate
        if not date or not time or not reason:
            raise InvalidAppointmentError("Date, time, and reason required")
        
        # Find resources
        patient = self.find_patient_by_id(patient_id)
        if not patient:
            raise PatientNotFoundError(patient_id)
        
        doctor = self.find_doctor_by_id(doctor_id)
        if not doctor:
            raise DoctorNotFoundError(doctor_id)
        
        room = self.find_room_by_id(room_id)
        if not room:
             raise RoomNotFoundError(room_id)
        
        # Check availability (Doctor)
        if not doctor.is_available(date, time):
            raise AppointmentConflictError(date, time, f"Dr. {doctor.name}")

        # Check availability (Room)
        if not room.is_available(date, time):
            raise AppointmentConflictError(date, time, f"Room {room.room_number}")
        
        # Create appointment (dependency injection)
        appointment = Appointment(date, time, reason, patient, doctor, room) 
        
        # Update schedules
        doctor.add_appointment(date, time)
        room.add_appointment(date, time) # Update room's schedule
        
        # Register appointment
        self._appointments[appointment.get_id()] = appointment
        
        return appointment
    
    def cancel_appointment(self, appointment_id: str) -> None:
        """Cancels an appointment and frees doctor's AND room's schedule."""
        appointment = self._appointments.get(appointment_id)
        if not appointment:
            raise InvalidAppointmentError("Appointment not found")
        
        appointment.cancel()
        appointment.doctor.remove_appointment(appointment.date, appointment.time)
        appointment.room.remove_appointment(appointment.date, appointment.time) # Clear room's schedule
        
    # ==================== STATISTICS ====================
    
    def get_total_appointments(self) -> int:
        """Returns total number of appointments."""
        return len(self._appointments)
    
    def get_active_appointments(self) -> int:
        """Returns count of active (scheduled) appointments."""
        return sum(
            1 for appt in self._appointments.values()
            if appt.status == "scheduled"
        )
    
    def __repr__(self):
        return (f"<Hospital: {self.name} | "
                f"Patients: {len(self._patients)}, "
                f"Doctors: {len(self._doctors)}, "
                f"Rooms: {len(self._rooms)}, "
                f"Appointments: {self.get_active_appointments()}>")
