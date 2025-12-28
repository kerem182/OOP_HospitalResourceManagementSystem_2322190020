# Hospital Resource Management System

**Assignment 2: Hospital Resource Management System**  
**Student:** Kerem Salih Erol (2322190020)  
**Course:** Object Based Programming (2019G0005)  
**Stage:** 2 - Basic Implementation

---

## 📋 Project Overview

This project implements a healthcare resource management system using Object-Oriented Programming (OOP) principles. The system models hospital operations including patient registration, doctor management, and appointment scheduling.

### Stage 2 Objectives

- Implement Hospital coordinator class with dependency injection
- Create appointment scheduling algorithm with conflict detection
- Add search algorithms for patients and doctors
- Implement custom exception handling
- Write comprehensive unit tests with mocking
- Apply encapsulation for internal state management

---

## 🏗️ Architecture Design (Stage 1)

### Design Principles Applied

#### 1. **Abstraction through Interfaces**

Two abstract base classes (ABCs) define contracts for domain entities:

* **`Identifiable`**: Enforces all domain entities to have unique identifiers
  + Used by: Patient, Doctor, Room, Appointment
  + Method: `get_id() -> str`

* **`Schedulable`**: Defines availability checking for schedulable resources
  + Used by: Doctor, Room
  + Method: `is_available(date: str, time: str) -> bool`

#### 2. **Composition Over Inheritance**

The `Appointment` class demonstrates composition by containing references to `Patient` and `Doctor` objects rather than inheriting from them. This creates a "has-a" relationship.

#### 3. **Encapsulation**

Each class encapsulates its own data and provides controlled access through methods:
- Private attributes store internal state (e.g., `_appointments`)
- Public methods expose necessary functionality
- `__repr__` methods provide readable object representation

---

## 📐 UML Class Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      <<Identifiable>>                            │
│                       <<interface>>                              │
│                                                                  │
│                    + get_id(): str                               │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ implements
                ┌─────────────┼────────────────┬─────────────┐
                │             │                │             │
                │             │                │             │
    ┌───────────┴──────┐  ┌──┴──────────┐  ┌──┴────────┐  ┌─┴────────────┐
    │     Patient      │  │   Doctor    │  │   Room    │  │ Appointment  │
    ├──────────────────┤  ├─────────────┤  ├───────────┤  ├──────────────┤
    │ - name: str      │  │ - name: str │  │ - room_   │  │ - date: str  │
    │ - patient_id:    │  │ - staff_id: │  │   number: │  │ - time: str  │
    │   str            │  │   str       │  │   int     │  │ - reason:    │
    │ - dob: str       │  │ - specialty:│  │ - capacity│  │   str        │
    │                  │  │   str       │  │   : int   │  │ - status:    │
    │                  │  │ - _appoint- │  │ - type:   │  │   str        │
    │                  │  │   ments:    │  │   str     │  │ - patient:   │
    │                  │  │   List      │  │           │  │   Patient ●──┐
    │                  │  │             │  │           │  │ - doctor:    │
    │                  │  │             │  │           │  │   Doctor  ●──┼─┐
    ├──────────────────┤  ├─────────────┤  ├───────────┤  ├──────────────┤ │
    │+ get_id(): str   │  │+ get_id():  │  │+ get_id():│  │+ get_id():   │ │
    └──────────────────┘  │  str        │  │  str      │  │  str         │ │
                          │+ is_available│ │+ is_      │  │+ cancel()    │ │
                          │  (): bool   │  │  available│  └──────────────┘ │
                          │+ add_appoint│  │  (): bool │         ▲         │
                          │  ment()     │  └───────────┘         │         │
                          │+ remove_    │        ▲               │         │
                          │  appointment│        │               │         │
                          └─────────────┘        │               │         │
                                  ▲              │               │         │
                                  │ implements   │               │         │
                                  │              │               │         │
                    ┌─────────────┴──────────────┘               │         │
                    │                                            │         │
         ┌──────────┴────────────┐                              │         │
         │   <<Schedulable>>      │                              │         │
         │    <<interface>>       │                              │         │
         │                        │                              │         │
         │ + is_available(date,   │                              │         │
         │   time): bool          │                              │         │
         └────────────────────────┘                              │         │
                                                                 │         │
                                                    Composition  │         │
                                                                 │         │
┌─────────────────────────────────────────────────────────────────────────┐│
│                          Hospital                                        ││
├──────────────────────────────────────────────────────────────────────────┤│
│ - name: str                                                              ││
│ - _patients: Dict[str, Patient]                                          ││
│ - _doctors: Dict[str, Doctor]                                            ││
│ - _appointments: Dict[str, Appointment]                                  ││
├──────────────────────────────────────────────────────────────────────────┤│
│ + register_patient(patient: Patient): None                               ││
│ + register_doctor(doctor: Doctor): None                                  ││
│ + find_patient_by_id(patient_id: str): Optional[Patient]                 ││
│ + find_doctor_by_id(doctor_id: str): Optional[Doctor]                    ││
│ + find_doctor_by_specialty(specialty: str): List[Doctor]                 ││
│ + schedule_appointment(patient_id, doctor_id, date, time, reason):       ││
│   Appointment                                                             ││
│ + cancel_appointment(appointment_id: str): None                          ││
│ + get_total_appointments(): int                                          ││
│ + get_active_appointments(): int                                         ││
└──────────────────────────────────────────────────────────────────────────┘│
                                    │                                       │
                                    │ manages                               │
                                    ▼                                       │
                    ┌───────────────────────────┐                          │
                    │   Patient, Doctor,        │◄─────────────────────────┘
                    │   Appointment (all)       │
                    └───────────────────────────┘


┌────────────────────────────────────────────────────────────────┐
│                    Custom Exceptions                            │
├────────────────────────────────────────────────────────────────┤
│                    HospitalError                                │
│                         ▲                                       │
│          ┌──────────────┼───────────────┬──────────────┐       │
│          │              │               │              │       │
│  PatientNotFound  DoctorNotFound  AppointmentConflict │       │
│      Error            Error           Error      InvalidError │
└────────────────────────────────────────────────────────────────┘


Legend:
  ▲        = implements (interface implementation)
  ●───>    = composition (strong ownership, filled diamond)
  ─────>   = association/dependency
  <<interface>> = abstract base class
```

---

## 🆕 Stage 2 Implementation

### New Components

#### 1. Hospital Coordinator Class (`hospital.py`)

The `Hospital` class is the central coordinator that manages all resources using **dependency injection** pattern.

**Key Responsibilities:**
- Register and manage patients and doctors
- Schedule and cancel appointments with validation
- Search for resources by various criteria
- Compute system statistics

**Main Methods:**
```python
hospital = Hospital("Istanbul Medical Center")

# Registration
hospital.register_patient(patient)
hospital.register_doctor(doctor)

# Scheduling
appointment = hospital.schedule_appointment(
    patient_id="P001",
    doctor_id="D001",
    date="2025-12-20",
    time="09:00",
    reason="Routine checkup"
)

# Searching
doctor = hospital.find_doctor_by_id("D001")
cardiologists = hospital.find_doctor_by_specialty("Cardiology")

# Statistics
total = hospital.get_total_appointments()
active = hospital.get_active_appointments()
```

#### 2. Appointment Scheduling Algorithm

**Method:** `Hospital.schedule_appointment()`

**Algorithm Steps:**
1. **Validate input data** - Check date, time, reason are not empty
2. **Find patient** - Lookup by ID, raise `PatientNotFoundError` if not found
3. **Find doctor** - Lookup by ID, raise `DoctorNotFoundError` if not found
4. **Check availability** - Verify doctor is free, raise `AppointmentConflictError` if busy
5. **Create appointment** - Instantiate with dependency injection
6. **Update schedule** - Add to doctor's appointment list
7. **Register** - Store in hospital's appointment registry
8. **Return** - Return created appointment object

**Complexity:** O(1) for all operations (hash map lookups)

**Example:**
```python
try:
    appointment = hospital.schedule_appointment(
        patient_id="P001",
        doctor_id="D001",
        date="2025-12-20",
        time="09:00",
        reason="Cardiac checkup"
    )
    print(f"Scheduled: {appointment}")
except PatientNotFoundError as e:
    print(f"Error: {e}")
except AppointmentConflictError as e:
    print(f"Conflict: {e}")
```

#### 3. Search Algorithms

**a) Search by ID** (O(1) complexity)
```python
patient = hospital.find_patient_by_id("P001")
doctor = hospital.find_doctor_by_id("D001")
```

**b) Search by Specialty** (O(n) complexity)
```python
cardiologists = hospital.find_doctor_by_specialty("Cardiology")
# Returns list of all doctors with matching specialty
```

**Implementation:** Linear search with case-insensitive substring matching

#### 4. Custom Exceptions (`exceptions.py`)

Domain-specific exceptions for better error handling:

| Exception | When Raised | Example |
|-----------|-------------|---------|
| `HospitalError` | Base exception | - |
| `PatientNotFoundError` | Patient ID doesn't exist | `PatientNotFoundError("P999")` |
| `DoctorNotFoundError` | Doctor ID doesn't exist | `DoctorNotFoundError("D999")` |
| `AppointmentConflictError` | Time slot already booked | `AppointmentConflictError(date, time, doctor)` |
| `InvalidAppointmentError` | Invalid appointment data | `InvalidAppointmentError("Missing data")` |

**Usage:**
```python
try:
    hospital.schedule_appointment(...)
except PatientNotFoundError as e:
    print(f"Patient not found: {e.patient_id}")
except AppointmentConflictError as e:
    print(f"Conflict on {e.date} at {e.time}")
```

#### 5. Enhanced Doctor Class

**New Features:**
- Tracks appointments in private `_appointments` list
- Real `is_available()` implementation checks actual schedule
- `add_appointment()` and `remove_appointment()` for schedule management

**Example:**
```python
doctor = Doctor("Dr. Coşkun Şahin", "D001", "Cardiology")

# Check availability
if doctor.is_available("2025-12-20", "09:00"):
    doctor.add_appointment("2025-12-20", "09:00")

# Later...
doctor.remove_appointment("2025-12-20", "09:00")
```

#### 6. Enhanced Appointment Class

**New Features:**
- `status` attribute tracks appointment state ("scheduled", "cancelled")
- `cancel()` method updates status
- Maintains composition with Patient and Doctor

**Example:**
```python
appointment = Appointment(date, time, reason, patient, doctor)
print(appointment.status)  # "scheduled"

appointment.cancel()
print(appointment.status)  # "cancelled"
```

---

## 🧪 Unit Tests (`tests/test_hospital.py`)

Comprehensive test suite with 10 essential tests:

### Test Coverage

| Test Class | Tests | Coverage |
|------------|-------|----------|
| `TestDoctor` | 1 test | Doctor availability checking |
| `TestAppointment` | 1 test | Composition pattern verification |
| `TestHospital` | 8 tests | Full hospital functionality |

### Key Tests

1. **test_doctor_availability** - Verifies scheduling updates availability
2. **test_appointment_composition** - Confirms Patient/Doctor composition
3. **test_register_patient** - Tests patient registration
4. **test_register_doctor** - Tests doctor registration
5. **test_search_by_specialty** - Validates search algorithm
6. **test_schedule_appointment_success** - Tests successful scheduling
7. **test_patient_not_found_error** - Validates PatientNotFoundError
8. **test_doctor_not_found_error** - Validates DoctorNotFoundError
9. **test_appointment_conflict_error** - Tests conflict detection
10. **test_cancel_appointment** - Verifies cancellation logic
11. **test_mock_example** - Demonstrates mocking with unittest.mock

### Running Tests

```bash
# Run all tests
python -m unittest tests.test_hospital -v

# Run specific test class
python -m unittest tests.test_hospital.TestHospital -v

# Run specific test
python -m unittest tests.test_hospital.TestHospital.test_schedule_appointment_success
```

### Mock Example

```python
def test_mock_example(self):
    """Test using mock for dependency injection."""
    hospital = Hospital("Test Hospital")
    
    # Create mock patient
    mock_patient = Mock(spec=Patient)
    mock_patient.get_id.return_value = "P001"
    
    # Inject mock
    hospital._patients["P001"] = mock_patient
    
    # Schedule and verify
    appointment = hospital.schedule_appointment(...)
    mock_patient.get_id.assert_called()
```

---

## 📁 Project Structure

```
OOP_HospitalResourceManagementSystem_2322190020/
│
├── app/
│   ├── __init__.py              # Package initialization
│   ├── identifiable.py          # Identifiable interface (Stage 1)
│   ├── schedulable.py           # Schedulable interface (Stage 1)
│   ├── patient.py               # Patient class (Stage 1)
│   ├── doctor.py                # Doctor class (updated Stage 2)
│   ├── room.py                  # Room class (Stage 1)
│   ├── appointment.py           # Appointment class (updated Stage 2)
│   ├── hospital.py              # NEW - Hospital coordinator
│   └── exceptions.py            # NEW - Custom exceptions
│
├── tests/
│   ├── __init__.py              # Tests package
│   └── test_hospital.py         # NEW - Unit tests (10 tests)
│
└── README.md                    # This file
```

---

## 🎯 OOP Principles Applied

### 1. Encapsulation

**Private Attributes:**
```python
class Doctor:
    def __init__(self, ...):
        self._appointments = []  # Private - cannot access directly
    
    def get_appointments(self):
        return self._appointments.copy()  # Controlled access
```

**Benefits:**
- Internal state protected from external modification
- Can change implementation without breaking API
- Maintains data integrity

### 2. Abstraction

**Interfaces:**
```python
class Identifiable(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass
```

**All entities implement common interfaces:**
- Patient, Doctor, Room, Appointment → `Identifiable`
- Doctor, Room → `Schedulable`

### 3. Composition

**Appointment contains Patient and Doctor:**
```python
class Appointment:
    def __init__(self, ..., patient: Patient, doctor: Doctor):
        self.patient = patient  # HAS-A relationship
        self.doctor = doctor    # HAS-A relationship
```

**Benefits:**
- Flexible relationships
- Independent lifecycles
- Easy to test with mocks

### 4. Dependency Injection

**Hospital coordinates without creating:**
```python
def schedule_appointment(self, patient_id, doctor_id, ...):
    patient = self.find_patient_by_id(patient_id)  # Inject
    doctor = self.find_doctor_by_id(doctor_id)    # Inject
    appointment = Appointment(..., patient, doctor)
```

**Benefits:**
- Loose coupling
- Easy to test (inject mocks)
- Centralized management

---

## 🚀 Usage Example

```python
from app.hospital import Hospital
from app.patient import Patient
from app.doctor import Doctor
from app.exceptions import AppointmentConflictError

# Create hospital
hospital = Hospital("Istanbul Medical Center")

# Register resources
patient1 = Patient("Kerem Salih Erol", "P001", "2005-02-18")
patient2 = Patient("Ayşe Yılmaz", "P002", "1992-05-10")
doctor = Doctor("Dr. Coşkun Şahin", "D001", "Cardiology")

hospital.register_patient(patient1)
hospital.register_patient(patient2)
hospital.register_doctor(doctor)

# Schedule appointments
try:
    appt1 = hospital.schedule_appointment(
        patient_id="P001",
        doctor_id="D001",
        date="2025-12-20",
        time="09:00",
        reason="Routine cardiac checkup"
    )
    print(f"✓ Scheduled: {appt1}")
    
    appt2 = hospital.schedule_appointment(
        patient_id="P002",
        doctor_id="D001",
        date="2025-12-20",
        time="09:00",  # Same time!
        reason="Follow-up"
    )
except AppointmentConflictError as e:
    print(f"✗ Conflict: {e}")

# Search
cardiologists = hospital.find_doctor_by_specialty("Cardiology")
print(f"Found {len(cardiologists)} cardiologist(s)")

# Statistics
print(f"Total appointments: {hospital.get_total_appointments()}")
print(f"Active appointments: {hospital.get_active_appointments()}")

# Cancel appointment
hospital.cancel_appointment(appt1.get_id())
print(f"Appointment status: {appt1.status}")  # "cancelled"
```

---

## 📊 Class Descriptions

### Core Classes (Stage 1)

#### `Patient`
- **Attributes:** `name`, `patient_id`, `dob`
- **Methods:** `get_id()`
- **Interface:** `Identifiable`

#### `Doctor`
- **Attributes:** `name`, `staff_id`, `specialty`, `_appointments` (private)
- **Methods:** `get_id()`, `is_available()`, `add_appointment()`, `remove_appointment()`
- **Interface:** `Identifiable`, `Schedulable`

#### `Room`
- **Attributes:** `room_number`, `capacity`, `type`
- **Methods:** `get_id()`, `is_available()` (placeholder)
- **Interface:** `Identifiable`, `Schedulable`

#### `Appointment`
- **Attributes:** `date`, `time`, `reason`, `patient`, `doctor`, `status`
- **Methods:** `get_id()`, `cancel()`
- **Interface:** `Identifiable`

### New Classes (Stage 2)

#### `Hospital`
- **Purpose:** Central coordinator managing all resources
- **Pattern:** Dependency Injection
- **Main Methods:**
  - `register_patient(patient)` - Register patient
  - `register_doctor(doctor)` - Register doctor
  - `schedule_appointment(...)` - Schedule with validation
  - `cancel_appointment(id)` - Cancel and free schedule
  - `find_patient_by_id(id)` - Search patient
  - `find_doctor_by_id(id)` - Search doctor
  - `find_doctor_by_specialty(specialty)` - Search by specialty
  - `get_total_appointments()` - Count all appointments
  - `get_active_appointments()` - Count active only

#### `Custom Exceptions`
- **`HospitalError`** - Base exception
- **`PatientNotFoundError`** - Patient not in system
- **`DoctorNotFoundError`** - Doctor not in system
- **`AppointmentConflictError`** - Time slot unavailable
- **`InvalidAppointmentError`** - Invalid data

---

## 📝 Stage 1 vs Stage 2 Changes

| Component | Stage 1 | Stage 2 |
|-----------|---------|---------|
| `Doctor.is_available()` | Returns `True` (placeholder) | Real schedule checking |
| `Doctor` attributes | No schedule tracking | `_appointments` list added |
| `Appointment` | Basic class | Added `status` and `cancel()` |
| Error handling | None | 5 custom exception types |
| Testing | None | 10 unit tests with mocks |
| Coordination | Manual object creation | Hospital coordinator class |
| Search | None | By ID and specialty |
| Statistics | None | Total and active counts |

---

## 🔜 Next Steps (Stage 3)

Stage 3 will add:

1. **Optimized Scheduling Algorithm**
   - Minimize waiting time
   - Maximize resource utilization

2. **Statistical Reports**
   - Doctor workload analysis
   - Average visit duration
   - Room occupancy rates

3. **Priority Queue**
   - Emergency patient prioritization
   - Triage system

4. **Web Interface**
   - Patient portal for appointments
   - Hospital management dashboard

5. **Data Persistence**
   - Save to JSON/database
   - Load historical data

---

## 📚 References

- Python ABC Module: https://docs.python.org/3/library/abc.html
- unittest.mock: https://docs.python.org/3/library/unittest.mock.html
- Course materials: cs01.pdf, cs02_01.pdf
- Assignment: Final Assignment Descriptions.pdf

---

## 👤 Author

**Kerem Salih Erol**  
Student ID: 2322190020  
Program: Software Engineering (English)  
Istanbul Esenyurt University

---

## 📝 Git Commit Message

```
feat(stage2): Implement Hospital coordinator, scheduling algorithm, and unit tests

- Add Hospital coordinator class with dependency injection pattern
- Implement 7-step appointment scheduling algorithm
- Add search algorithms (by ID and specialty)
- Create 5 custom exception types for domain errors
- Update Doctor class with real scheduling functionality
- Update Appointment class with status management
- Add 10 unit tests including mocking examples
- Update README with Stage 2 documentation

Stage 2 requirements completed:
✓ Hospital coordinator managing associations
✓ Scheduling and cancellation behaviors
✓ Search algorithm (ID, specialty)
✓ Custom exceptions (PatientNotFound, DoctorNotFound, Conflict, Invalid)
✓ Encapsulation (private _appointments)
✓ Unit tests with unittest.mock
✓ Statistics computation (active appointments)
```

---

**Last Updated:** December 19, 2024  
**Stage:** 2 - Basic Implementation  
**Status:** ✅ Complete
