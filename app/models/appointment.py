from .identifiable import Identifiable
from .patient import Patient
from .doctor import Doctor

class Appointment(Identifiable):
    """
    Represents a medical appointment.
    """
    def __init__(self, date: str, time: str, reason: str, patient: Patient, doctor: Doctor):
        self.date = date
        self.time = time
        self.reason = reason
        self.patient = patient
        self.doctor = doctor

    def get_id(self) -> str:
        return f"{self.date}_{self.time}_{self.patient.get_id()}"

    def __repr__(self):
        return f"<Appointment: {self.date} / {self.doctor.specialty} ({self.patient.name})>"