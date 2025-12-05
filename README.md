# Hospital Resource Management System

**Assignment 2: Hospital Resource Management System**  
**Student:** Kerem Salih Erol (2322190020)  
**Course:** Object Based Programming (2019G0005)  
**Stage:** 1 - Architecture Design

---

## 📋 Project Overview

This project implements a healthcare resource management system using Object-Oriented Programming (OOP) principles. The system models hospital operations including patient registration, doctor management, room allocation, and appointment scheduling.

### Objectives
- Apply core OOP principles: abstraction, encapsulation, inheritance, and composition
- Design a scalable and maintainable healthcare management platform
- Implement clean architecture with well-defined interfaces and domain classes

---

## 🏗️ Architecture Design

### Design Principles Applied

#### 1. **Abstraction through Interfaces**
Two abstract base classes (ABCs) define contracts for domain entities:

- **`Identifiable`**: Enforces all domain entities to have unique identifiers
  - Used by: Patient, Doctor, Room, Appointment
  - Method: `get_id() -> str`

- **`Schedulable`**: Defines availability checking for schedulable resources
  - Used by: Doctor, Room
  - Method: `is_available(date: str, time: str) -> bool`

#### 2. **Composition Over Inheritance**
The `Appointment` class demonstrates composition by containing references to `Patient` and `Doctor` objects rather than inheriting from them. This creates a "has-a" relationship:
- An Appointment **has a** Patient
- An Appointment **has a** Doctor

This design allows:
- Flexible associations between entities
- Independent lifecycle management
- Easier testing and modification

#### 3. **Encapsulation**
Each class encapsulates its own data and provides controlled access through methods:
- Private attributes store internal state
- Public methods expose necessary functionality
- `__repr__` methods provide readable object representation

---

## 📐 UML Class Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      <<Identifiable>>                        │
│                         <<interface>>                        │
│                                                              │
│                      + get_id(): str                         │
└─────────────────────────────────────────────────────────────┘
                                ▲
                                │ implements
                ┌───────────────┼───────────────┬──────────────┐
                │               │               │              │
                │               │               │              │
┌───────────────┴────┐  ┌───────┴────────┐  ┌──┴─────────┐  ┌─┴────────────┐
│     Patient        │  │     Doctor     │  │   Room     │  │ Appointment  │
├────────────────────┤  ├────────────────┤  ├────────────┤  ├──────────────┤
│ - name: str        │  │ - name: str    │  │ - room_    │  │ - date: str  │
│ - patient_id: str  │  │ - staff_id:    │  │   number:  │  │ - time: str  │
│ - dob: str         │  │   str          │  │   int      │  │ - reason:    │
│                    │  │ - specialty:   │  │ - capacity:│  │   str        │
│                    │  │   str          │  │   int      │  │ - patient:   │
│                    │  │                │  │ - type: str│  │   Patient    │
│                    │  │                │  │            │  │ - doctor:    │
│                    │  │                │  │            │  │   Doctor     │
├────────────────────┤  ├────────────────┤  ├────────────┤  ├──────────────┤
│ + get_id(): str    │  │ + get_id(): str│  │ + get_id():│  │ + get_id():  │
└────────────────────┘  │ + is_available │  │   str      │  │   str        │
                        │   (): bool     │  │ + is_      │  └──────────────┘
                        └────────────────┘  │   available│
                                            │   (): bool │
                                            └────────────┘
                                ▲                    ▲
                                │ implements         │
                                │                    │
                        ┌───────┴────────────────────┘
                        │
         ┌──────────────┴──────────────────┐
         │      <<Schedulable>>             │
         │       <<interface>>              │
         │                                  │
         │  + is_available(date: str,       │
         │    time: str): bool              │
         └──────────────────────────────────┘


┌─────────────────────────────────────────────────────────────┐
│                      Appointment                             │
├─────────────────────────────────────────────────────────────┤
│ - date: str                                                  │
│ - time: str                                                  │
│ - reason: str                                                │
│ - patient: Patient    ●────────────┐                         │
│ - doctor: Doctor      ●────────┐   │                         │
├─────────────────────────────────┼───┼─────────────────────────┤
│ + get_id(): str                 │   │                         │
└─────────────────────────────────┼───┼─────────────────────────┘
                                  │   │
                         (composition)│
                                  │   │
                                  ▼   ▼
                              Doctor Patient
                              
Legend:
  ▲        = implements (inheritance/interface implementation)
  ●────>   = composition (strong ownership, filled diamond)
  ─────>   = association (weak relationship)
```

---

---

## 🔧 Class Descriptions

### Abstract Base Classes (Interfaces)

#### `Identifiable`
```python
class Identifiable(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass
```
- **Purpose**: Ensures all domain entities have unique identifiers
- **Implementing classes**: Patient, Doctor, Room, Appointment

#### `Schedulable`
```python
class Schedulable(ABC):
    @abstractmethod
    def is_available(self, date: str, time: str) -> bool:
        pass
```
- **Purpose**: Provides contract for availability checking
- **Implementing classes**: Doctor, Room
- **Note**: Stage 1 returns `True` by default; Stage 2 will implement real scheduling logic

### Domain Classes

#### `Patient`
Represents a patient in the hospital system.

**Attributes:**
- `name: str` - Patient's full name
- `patient_id: str` - Unique patient identifier
- `dob: str` - Date of birth

**Methods:**
- `get_id() -> str` - Returns unique patient ID
- `__repr__()` - Returns readable representation

**Example:**
```python
patient = Patient("Ali Yılmaz", "P12345", "1990-05-15")
print(patient.get_id())  # "P12345"
```

#### `Doctor`
Represents a doctor in the hospital.

**Attributes:**
- `name: str` - Doctor's full name
- `staff_id: str` - Unique staff identifier
- `specialty: str` - Medical specialty (e.g., "Cardiology", "Neurology")

**Methods:**
- `get_id() -> str` - Returns staff ID
- `is_available(date, time) -> bool` - Checks availability (placeholder in Stage 1)
- `__repr__()` - Returns readable representation

**Example:**
```python
doctor = Doctor("Ayşe Demir", "D001", "Cardiology")
print(doctor.is_available("2024-12-10", "14:00"))  # True
```

#### `Room`
Represents a physical hospital room.

**Attributes:**
- `room_number: int` - Unique room number
- `capacity: int` - Maximum occupancy
- `type: str` - Room type (e.g., "Surgery Room", "ICU", "Standard")

**Methods:**
- `get_id() -> str` - Returns room number as string
- `is_available(date, time) -> bool` - Checks availability (placeholder in Stage 1)
- `__repr__()` - Returns readable representation

**Example:**
```python
room = Room(101, 1, "Surgery Room")
print(room.get_id())  # "101"
```

#### `Appointment`
Represents a medical appointment (composition example).

**Attributes:**
- `date: str` - Appointment date
- `time: str` - Appointment time
- `reason: str` - Reason for appointment
- `patient: Patient` - Associated patient (composition)
- `doctor: Doctor` - Associated doctor (composition)

**Methods:**
- `get_id() -> str` - Returns unique compound identifier
- `__repr__()` - Returns readable representation

**Example:**
```python
appointment = Appointment(
    date="2024-12-10",
    time="14:00",
    reason="Routine checkup",
    patient=patient,
    doctor=doctor
)
print(appointment.get_id())  # "2024-12-10_14:00_P12345"
```

---

## 🚀 Usage Example

```python
if __name__ == "__main__":
    # Create domain objects
    p = Patient("Kerem", "P001", "2005-02-18")
    d = Doctor("Coşkun Şahin", "D001", "Cardiology")
    r = Room(101, 2, "ICU")
    
    # Create an appointment using the patient and doctor objects
    # This demonstrates COMPOSITION in action
    a = Appointment("2025-12-05", "14:00", "Checkup", p, d)

    # Display all objects
    print(p)  # <Patient: Kerem (P001)>
    print(d)  # <Doctor: Dr. Coşkun Şahin (Cardiology)>
    print(r)  # <Room: 101 (ICU)>
    print(a)  # <Appointment: 2025-12-05 / Cardiology (Kerem)>
    print("Appointment ID:", a.get_id())  # 2025-12-05_14:00_P001
    
    # Check availability (placeholder in Stage 1)
    print("Doctor available?", d.is_available("2025-12-05", "14:00"))  # True
    print("Room available?", r.is_available("2025-12-05", "14:00"))    # True
```

**Expected Output:**
```
<Patient: Kerem (P001)>
<Doctor: Dr. Coşkun Şahin (Cardiology)>
<Room: 101 (ICU)>
<Appointment: 2025-12-05 / Cardiology (Kerem)>
Appointment ID: 2025-12-05_14:00_P001
Doctor available? True
Room available? True
```

---

## 📊 Design Decisions

### Why Abstract Base Classes?
1. **Contract enforcement**: Ensures all entities implement required methods
2. **Polymorphism support**: Allows treating different objects through common interfaces
3. **Type safety**: Enables static type checking with tools like mypy
4. **Documentation**: ABCs serve as explicit documentation of expected behavior

### Why Composition for Appointments?
1. **Flexibility**: Patients and doctors exist independently of appointments
2. **Reusability**: Same patient/doctor can be in multiple appointments
3. **Lifecycle independence**: Deleting an appointment doesn't delete the patient or doctor
4. **Testing**: Easy to mock Patient/Doctor objects for appointment testing

### Relationships Summary
| Relationship Type | Example | Explanation |
|------------------|---------|-------------|
| **Interface Implementation** | Doctor → Identifiable | Doctor implements the Identifiable contract |
| **Interface Implementation** | Doctor → Schedulable | Doctor implements the Schedulable contract |
| **Composition** | Appointment → Patient | Appointment contains a Patient reference |
| **Composition** | Appointment → Doctor | Appointment contains a Doctor reference |

---

## 📁 Project Structure

```
OOP_HospitalSystem_2322190020/
├── README.md                 # This file
├── hospital_system.py        # Main implementation (Stage 1)
├── docs/
│   └── class_diagram.png     # UML class diagram
└── tests/
    └── (to be added in Stage 2)
```

---

## 🎯 Stage 1 Deliverables Checklist

- [x] Define core classes: Patient, Doctor, Room, Appointment
- [x] Apply abstraction through Identifiable and Schedulable interfaces
- [x] Implement composition (Appointment contains Patient and Doctor)
- [x] Use encapsulation for attributes and methods
- [x] Add documentation with docstrings
- [x] Create UML/Class diagram (see docs/)
- [x] Write comprehensive README

---

## 🔜 Next Steps (Stage 2 & 3)

### Stage 2: Basic Implementation
- Implement scheduling and cancellation logic
- Add real availability checking in `is_available()` methods
- Implement search algorithms (by ID, name, specialty)
- Add automated unit tests with mocking
- Create Hospital coordinator class for dependency injection
- Custom exceptions (e.g., `InvalidAppointmentError`)

### Stage 3: Advanced Application
- Optimized scheduling algorithm (minimize waiting time)
- Statistical reports (doctor workload, occupancy rate)
- Priority-based queue for emergency patients
- Web interface for patients and hospital management
- Data persistence (JSON/database)

---

## 📚 References

- Course materials: Introduction to OOP (cs01, cs02_01)
- Assignment description: Final Assignment Descriptions.pdf
- Python ABC documentation: https://docs.python.org/3/library/abc.html

---

## 👤 Author

**Kerem Salih Erol**  
Student ID: 2322190020  
Program: Software Engineering (English)  
Istanbul Esenyurt University

---

## 📝 License

This project is submitted as part of academic coursework for Object Based Programming course.

---

**Last Updated:** December 5, 2024  
**Stage:** 1 - Architecture Design  
**Status:** ✅ Complete
