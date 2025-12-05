from abc import ABC, abstractmethod

# -------------------------------------------------------
# ABSTRACT BASE CLASSES (INTERFACES)
# -------------------------------------------------------

class Identifiable(ABC):
    """
    An abstract interface that enforces every domain entity
    to have a unique identifier through get_id().
    """
    @abstractmethod
    def get_id(self) -> str:
        pass


class Schedulable(ABC):
    """
    Abstract interface for objects that can be checked
    for availability (e.g., doctors, rooms).
    This will be useful for Stage 2 scheduling algorithms.
    """
    @abstractmethod
    def is_available(self, date: str, time: str) -> bool:
        pass


# -------------------------------------------------------
# DOMAIN CLASSES
# -------------------------------------------------------

class Patient(Identifiable):
    """
    Represents a patient in the hospital system.
    Implements Identifiable to ensure it has a unique patient ID.
    """
    def __init__(self, name: str, patient_id: str, dob: str):
        self.name = name
        self.patient_id = patient_id
        self.dob = dob  # date of birth

    def get_id(self) -> str:
        """Returns the unique patient ID."""
        return self.patient_id

    def __repr__(self):
        return f"<Patient: {self.name} ({self.patient_id})>"


class Doctor(Identifiable, Schedulable):
    """
    Represents a doctor in the hospital.
    - Identifiable: must have an ID (staff_id)
    - Schedulable: must support scheduling availability checks
    """
    def __init__(self, name: str, staff_id: str, specialty: str):
        self.name = name
        self.staff_id = staff_id
        self.specialty = specialty

    def get_id(self) -> str:
        """Returns the unique staff ID of the doctor."""
        return self.staff_id

    def is_available(self, date: str, time: str) -> bool:
        """
        Stage 1: Simple placeholder.
        Stage 2: Will check real availability.
        """
        return True  

    def __repr__(self):
        return f"<Doctor: Dr. {self.name} ({self.specialty})>"


class Room(Identifiable, Schedulable):
    """
    Represents a physical hospital room.
    Rooms also implement Schedulable for future time-slot control.
    """
    def __init__(self, room_number: int, capacity: int, type: str):
        self.room_number = room_number
        self.capacity = capacity
        self.type = type  # e.g., Surgery Room, ICU, Standard

    def get_id(self) -> str:
        """Returns the room number as its unique ID."""
        return str(self.room_number)

    def is_available(self, date: str, time: str) -> bool:
        """
        Stage 1: Always returns True.
        Stage 2: Room scheduling rules can be added.
        """
        return True

    def __repr__(self):
        return f"<Room: {self.room_number} ({self.type})>"


class Appointment(Identifiable):
    """
    Represents a medical appointment.
    Demonstrates COMPOSITION:
    - An Appointment 'has a' Patient
    - An Appointment 'has a' Doctor
    """
    def __init__(self, date: str, time: str, reason: str, patient: Patient, doctor: Doctor):
        self.date = date
        self.time = time
        self.reason = reason

        # Composition relationship
        self.patient = patient
        self.doctor = doctor

    def get_id(self) -> str:
        """
        Unique appointment identifier combining
        date, time, and patient ID.
        """
        return f"{self.date}_{self.time}_{self.patient.get_id()}"

    def __repr__(self):
        return f"<Appointment: {self.date} / {self.doctor.specialty} ({self.patient.name})>"

if __name__ == "__main__":
    p = Patient("Kerem", "P001", "2005-02-18")
    d = Doctor("Coşkun Şahin", "D001", "Cardiology")
    r = Room(101, 2, "ICU")
    
    # Create an appointment using the patient and doctor objects
    a = Appointment("2025-12-05", "14:00", "Checkup", p, d)

    print(p)
    print(d)
    print(r)
    print(a)
    print("Appointment ID:", a.get_id())
