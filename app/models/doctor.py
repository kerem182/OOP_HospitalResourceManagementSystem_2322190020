from .identifiable import Identifiable
from .schedulable import Schedulable

class Doctor(Identifiable, Schedulable):
    """
    Represents a doctor in the hospital.
    """
    def __init__(self, name: str, staff_id: str, specialty: str):
        self.name = name
        self.staff_id = staff_id
        self.specialty = specialty

    def get_id(self) -> str:
        return self.staff_id

    def is_available(self, date: str, time: str) -> bool:
        return True

    def __repr__(self):
        return f"<Doctor: Dr. {self.name} ({self.specialty})>"