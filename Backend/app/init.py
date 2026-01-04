"""
Hospital Resource Management System - Application Package
Stage 2: Basic Implementation
"""

from .identifiable import Identifiable
from .schedulable import Schedulable
from .patient import Patient
from .doctor import Doctor
from .room import Room
from .appointment import Appointment
from .hospital import Hospital
from .exceptions import (
    HospitalError,
    PatientNotFoundError,
    DoctorNotFoundError,
    AppointmentConflictError,
    InvalidAppointmentError
)

__all__ = [
    'Identifiable',
    'Schedulable',
    'Patient',
    'Doctor',
    'Room',
    'Appointment',
    'Hospital',
    'HospitalError',
    'PatientNotFoundError',
    'DoctorNotFoundError',
    'AppointmentConflictError',
    'InvalidAppointmentError',
]