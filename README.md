# Hospital Resource Management System

**Assignment 2: Hospital Resource Management System**  
**Student:** Kerem Salih Erol (2322190020)  
**Course:** Object Based Programming (2019G0005)  
**Stage:** 3 - Advanced Application

---

## Project Overview

This project implements a healthcare resource management system using Object-Oriented Programming principles. The system manages hospital operations including patient registration, doctor scheduling, room allocation, and appointment coordination with intelligent workload optimization and priority-based scheduling.

The implementation fulfills all requirements specified in Assignment 2, progressing through three development stages: architectural design, basic implementation, and advanced algorithmic features with web-based reporting.

---

## Architecture Design

### Design Principles Applied

**Abstraction through Interfaces**

Two abstract base classes define contracts for domain entities:

- `Identifiable`: Enforces unique identifiers for all entities (Patient, Doctor, Room, Appointment)
- `Schedulable`: Defines availability checking for schedulable resources (Doctor, Room)

**Composition Over Inheritance**

The `Appointment` class demonstrates composition by containing references to `Patient`, `Doctor`, and `Room` objects rather than inheriting from them.

**Encapsulation**

Each class encapsulates its own data and provides controlled access through methods. Private attributes (`_appointments`, `_patients`, `_doctors`, `_rooms`, `_reservations`) store internal state with public methods exposing necessary functionality.

**Dependency Injection**

The `Hospital` coordinator class manages associations without creating dependencies, enabling loose coupling and simplified testing.

---

## UML Class Diagram

```
                    <<Identifiable>>
                    + get_id(): str
                           ▲
        ┌──────────────────┼──────────────────┐
        │                  │                  │
    Patient           Doctor            Appointment
    - name            - name            - date
    - patient_id      - staff_id        - time
    - dob             - specialty       - reason
                      - _appointments   - status
    + get_id()        + get_id()        - patient: Patient ●──┐
                      + is_available()  - doctor: Doctor   ●──┼─┐
                      + add_appointment()                      │ │
                                                    Room       │ │
                                                    - room_number
                                                    - capacity │ │
                                                    - type     │ │
                    <<Schedulable>>               - _reservations
                    + is_available()                + get_id()│ │
                           ▲                        + is_available()
                           │                        + add_reservation()
                    ┌──────┴──────┐                            │ │
                    │             │                            │ │
                 Doctor         Room                           │ │
                                                               │ │
┌──────────────────────────────────────────────────────────────┘ │
│                          Hospital                               │
├─────────────────────────────────────────────────────────────────┤
│ - name: str                                                     │
│ - _patients: Dict[str, Patient]                                 │
│ - _doctors: Dict[str, Doctor]                                   │
│ - _rooms: Dict[str, Room]                                       │
│ - _appointments: Dict[str, Appointment]                         │
├─────────────────────────────────────────────────────────────────┤
│ + register_patient(patient)                                     │
│ + register_doctor(doctor)                                       │
│ + register_room(room)                                           │
│ + find_least_busy_doctor(specialty): Doctor                     │
│ + schedule_appointment_optimized(...): Appointment              │
│ + cancel_appointment(id)                                        │
│ + get_doctor_workload_report(): Dict                            │
│ + get_room_occupancy_report(): Dict                             │
│ + get_specialty_report(): Dict                                  │
│ + get_overall_statistics(): Dict                                │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ manages
                           ▼
            ┌──────────────────────────┐
            │ Patient, Doctor, Room,   │◄─────────────────────────┘
            │ Appointment (all)        │
            └──────────────────────────┘


        Custom Exceptions
        
        HospitalError (base)
             ▲
             ├── PatientNotFoundError
             ├── DoctorNotFoundError
             ├── RoomNotFoundError
             ├── AppointmentConflictError
             └── InvalidAppointmentError
```

---

## Stage 3 Advanced Algorithms

### 1. Workload Balancing Algorithm

**Method:** `Hospital.find_least_busy_doctor(specialty: str)`

Automatically selects the doctor with the fewest active appointments within a requested medical specialty.

**Algorithm:**
1. Retrieve all doctors matching the specified specialty
2. Return None if no doctors found
3. Count active appointments for each doctor
4. Return doctor with minimum workload

**Complexity:** O(n×m) where n = doctors, m = appointments

```python
def find_least_busy_doctor(self, specialty: str) -> Optional[Doctor]:
    doctors = self.find_doctor_by_specialty(specialty)
    if not doctors:
        return None
    
    min_workload = float('inf')
    least_busy_doctor = None
    
    for doctor in doctors:
        workload = sum(
            1 for appt in self._appointments.values()
            if appt.doctor.get_id() == doctor.get_id() 
            and appt.status == "scheduled"
        )
        
        if workload < min_workload:
            min_workload = workload
            least_busy_doctor = doctor
    
    return least_busy_doctor
```

### 2. Optimized Appointment Scheduling

**Method:** `Hospital.schedule_appointment_optimized()`

Schedules appointments with automatic doctor selection based on workload optimization.

**Algorithm:**
1. Validate input data
2. Find patient and room by ID
3. **Call workload balancing algorithm** to find least busy doctor
4. Check doctor and room availability
5. Create appointment with dependency injection
6. Update doctor's and room's schedules
7. Register appointment

**Complexity:** O(d×a) where d = doctors in specialty, a = appointments

### 3. Priority-Based Queue System

**Priority Levels:**
- **HIGH:** Cardiology appointments (time-sensitive)
- **MEDIUM:** General medical appointments
- **LOW:** Routine checkups

Priority classification is integrated into web interface sorting, ensuring critical cases receive immediate attention.

---

## Statistical Reporting

### 1. Doctor Workload Report

**Method:** `get_doctor_workload_report()`

Returns detailed statistics for each doctor including total appointments, active appointments, cancelled appointments, and occupancy rate.

**Complexity:** O(d×a)

### 2. Room Occupancy Report

**Method:** `get_room_occupancy_report()`

Returns occupancy statistics for each room including reservation count and occupancy percentage.

**Complexity:** O(r)

### 3. Specialty-Based Report

**Method:** `get_specialty_report()`

Groups appointments by medical specialty and generates comparative statistics.

**Complexity:** O(s×a)

### 4. Overall Hospital Statistics

**Method:** `get_overall_statistics()`

Returns system-wide metrics including total resources, appointments, and cancellation rate.

**Complexity:** O(a)

---

## Enhanced Room Management

**New Features in Room Class:**

- `_reservations`: Private list tracking scheduled time slots
- `is_available(date, time)`: Checks room availability
- `add_reservation(date, time)`: Reserves time slot
- `remove_reservation(date, time)`: Frees time slot during cancellation

Rooms are now fully integrated with the scheduling system, preventing double-booking and enabling proper resource tracking.

---

## Web Interface (Streamlit)

**File:** `app_web.py`

**Key Features:**

**Dashboard Metrics**
- Total patients, doctors, active appointments
- Cancellation rate with indicators

**Visual Analytics**
- Doctor workload bar chart
- Room occupancy bar chart
- Detailed statistics tables
- Specialty-based dataframe

**Smart Appointment Booking**
- Patient selection dropdown
- Specialty selection (auto-assigns least busy doctor)
- Room and time slot selection
- Validation and error handling

**Appointment Management**
- Filterable appointment list (All/Scheduled/Cancelled)
- Cancellation workflow with resource cleanup

**Session State Management**
- Data persists across page interactions
- No data loss on form submissions

---

## Project Structure

```
HOSPITAL_RESOURCE_MANAGEMENT_SYSTEM/
│
├── Backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── identifiable.py          # Identifiable interface
│   │   ├── schedulable.py           # Schedulable interface
│   │   ├── patient.py               # Patient entity
│   │   ├── doctor.py                # Doctor with scheduling
│   │   ├── room.py                  # Room with reservations
│   │   ├── appointment.py           # Appointment composition
│   │   ├── hospital.py              # Hospital coordinator
│   │   └── exceptions.py            # Custom exceptions
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_hospital.py         # Unit tests with mocking
│   │
│   ├── app_web.py                   # Streamlit web interface
│   └── demo.py                      # Command-line demonstration
│
├── .gitignore
└── README.md
```

---

## Installation and Usage

### Prerequisites

Python 3.8 or higher

### Installation

```bash
git clone https://github.com/drcoskuns/OOP_HospitalResourceManagementSystem_2322190020.git
cd HOSPITAL_RESOURCE_MANAGEMENT_SYSTEM/Backend
pip install streamlit pandas
```

### Running the Application

**Web Dashboard:**
```bash
python -m streamlit run app_web.py
```
Access at `http://localhost:8501`

**Command-Line Demo:**
```bash
python demo.py
```

**Unit Tests:**
```bash
python -m unittest tests.test_hospital -v
```

---

## OOP Principles Applied

### Encapsulation

Private attributes with controlled access:

```python
class Hospital:
    def __init__(self, name: str):
        self._patients: Dict[str, Patient] = {}
        self._doctors: Dict[str, Doctor] = {}
```

### Abstraction

Interfaces enforce contracts:

```python
class Identifiable(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass
```

### Composition

Appointment contains references:

```python
class Appointment:
    def __init__(self, ..., patient: Patient, doctor: Doctor, room: Room):
        self.patient = patient  # HAS-A
        self.doctor = doctor    # HAS-A
        self.room = room        # HAS-A
```

### Dependency Injection

Hospital injects existing resources:

```python
def schedule_appointment(self, patient_id, doctor_id, room_id, ...):
    patient = self.find_patient_by_id(patient_id)
    doctor = self.find_doctor_by_id(doctor_id)
    room = self.find_room_by_id(room_id)
    appointment = Appointment(..., patient, doctor, room)
```

---

## Exception Handling

**Custom Exception Hierarchy:**

```python
HospitalError
├── PatientNotFoundError
├── DoctorNotFoundError
├── RoomNotFoundError
├── AppointmentConflictError
└── InvalidAppointmentError
```

**Usage:**

```python
try:
    hospital.schedule_appointment(...)
except PatientNotFoundError as e:
    print(f"Patient {e.patient_id} not found")
except AppointmentConflictError as e:
    print(f"Conflict on {e.date} at {e.time}")
```

---

## Testing

**Test Suite:** 10 comprehensive unit tests

**Coverage:**
- Doctor availability checking
- Appointment composition verification
- Patient and doctor registration
- Search algorithms
- Scheduling success and conflict scenarios
- Exception validation
- Cancellation workflow
- Mock-based dependency injection

**Run tests:**
```bash
python -m unittest tests.test_hospital -v
```

---

## Stage Development Summary

**Stage 1: Architecture Design**
- Defined core domain classes and interfaces
- Established composition-based relationships
- Created UML class diagrams

**Stage 2: Basic Implementation**
- Implemented Hospital coordinator class
- Added scheduling algorithm with conflict detection
- Developed search functionality
- Created custom exception hierarchy
- Wrote 10 unit tests with mocking

**Stage 3: Advanced Application**
- Developed workload balancing algorithm
- Implemented optimized scheduling
- Created statistical reporting methods
- Enhanced Room class with reservation tracking
- Built Streamlit web dashboard
- Added visual analytics and priority-based display

---

## Algorithm Complexity Summary

| Algorithm | Method | Complexity |
|-----------|--------|------------|
| Find least busy doctor | `find_least_busy_doctor()` | O(n×m) |
| Optimized scheduling | `schedule_appointment_optimized()` | O(d×a) |
| Doctor workload report | `get_doctor_workload_report()` | O(d×a) |
| Room occupancy report | `get_room_occupancy_report()` | O(r) |
| Specialty report | `get_specialty_report()` | O(s×a) |
| Overall statistics | `get_overall_statistics()` | O(a) |

---

## Usage Example

```python
from app.hospital import Hospital
from app.patient import Patient
from app.doctor import Doctor
from app.room import Room

# Create hospital
hospital = Hospital("Istanbul Medical Center")

# Register resources
patient = Patient("Kerem Salih Erol", "P001", "2005-02-18")
doctor1 = Doctor("Dr. Coşkun Şahin", "D001", "Cardiology")
doctor2 = Doctor("Dr. Ayşe Demir", "D002", "Cardiology")
room = Room(101, 1, "Surgery Room")

hospital.register_patient(patient)
hospital.register_doctor(doctor1)
hospital.register_doctor(doctor2)
hospital.register_room(room)

# Optimized scheduling (auto-select least busy doctor)
appt = hospital.schedule_appointment_optimized(
    patient_id="P001",
    specialty="Cardiology",
    room_id="101",
    date="2025-12-21",
    time="09:00",
    reason="Cardiac assessment"
)

print(f"Assigned to: {appt.doctor.name}")

# Get statistics
stats = hospital.get_overall_statistics()
print(f"Total appointments: {stats['total_appointments']}")
```

---

## Author

**Kerem Salih Erol**  
Student ID: 2322190020  
Program: Software Engineering (English)  
Istanbul Esenyurt University

---

**Last Updated:** January 4, 2025  
**Stage:** 3 - Advanced Application  
**Status:** Complete
