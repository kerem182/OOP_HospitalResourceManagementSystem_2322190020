"""
Custom exceptions for Hospital Resource Management System.
Stage 2: Minimal essential exceptions.
Stage 3: Added RoomNotFoundError.
"""


class HospitalError(Exception):
    """Base exception for all hospital-related errors."""
    pass


class PatientNotFoundError(HospitalError):
    """Raised when a patient cannot be found in the system."""
    def __init__(self, patient_id: str):
        self.patient_id = patient_id
        super().__init__(f"Patient with ID '{patient_id}' not found")


class DoctorNotFoundError(HospitalError):
    """Raised when a doctor cannot be found in the system."""
    def __init__(self, doctor_id: str):
        self.doctor_id = doctor_id
        super().__init__(f"Doctor with ID '{doctor_id}' not found")


class RoomNotFoundError(HospitalError):
    """Raised when a room cannot be found in the system."""
    def __init__(self, room_id: str):
        self.room_id = room_id
        super().__init__(f"Room with ID '{room_id}' not found")


class AppointmentConflictError(HospitalError):
    """Raised when scheduling conflicts with existing appointment."""
    def __init__(self, date: str, time: str, resource: str):
        self.date = date
        self.time = time
        super().__init__(
            f"{resource} is not available on {date} at {time}"
        )


class InvalidAppointmentError(HospitalError):
    """Raised when appointment data is invalid."""
    pass