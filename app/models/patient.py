from .identifiable import Identifiable

class Patient(Identifiable):
    """
    Represents a patient in the hospital system.
    """
    def __init__(self, name: str, patient_id: str, dob: str):
        self.name = name
        self.patient_id = patient_id
        self.dob = dob

    def get_id(self) -> str:
        return self.patient_id

    def __repr__(self):
        return f"<Patient: {self.name} ({self.patient_id})>"