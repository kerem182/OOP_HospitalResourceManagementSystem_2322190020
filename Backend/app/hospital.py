"""
Hospital coordinator class - manages all resources.
Stage 3: Advanced algorithms and statistical reporting.
"""
from typing import Dict, List, Optional
from .patient import Patient
from .doctor import Doctor
from .room import Room
from .appointment import Appointment
from .exceptions import (
    PatientNotFoundError,
    DoctorNotFoundError,
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
        self._rooms: Dict[str, Room] = {}
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
    
    # ==================== STAGE 3: WORKLOAD OPTIMIZATION ====================
    
    def find_least_busy_doctor(self, specialty: str) -> Optional[Doctor]:
        """
        Finds the doctor with the least workload (fewest appointments) 
        in a given specialty.
        
        Algorithm: Workload Balancing
        1. Get all doctors with the specified specialty
        2. Count active appointments for each doctor
        3. Return the doctor with minimum workload
        
        Args:
            specialty: Medical specialty to search
            
        Returns:
            Doctor with least workload, or None if no doctors found
            
        Complexity: O(n*m) where n=doctors, m=appointments
        """
        # Get all doctors with this specialty
        doctors = self.find_doctor_by_specialty(specialty)
        
        if not doctors:
            return None
        
        # Calculate workload for each doctor
        min_workload = float('inf')
        least_busy_doctor = None
        
        for doctor in doctors:
            # Count active appointments for this doctor
            workload = sum(
                1 for appt in self._appointments.values()
                if appt.doctor.get_id() == doctor.get_id() 
                and appt.status == "scheduled"
            )
            
            # Update if this doctor has less workload
            if workload < min_workload:
                min_workload = workload
                least_busy_doctor = doctor
        
        return least_busy_doctor
    
    def schedule_appointment_optimized(
        self,
        patient_id: str,
        specialty: str,
        room_id: str,
        date: str,
        time: str,
        reason: str
    ) -> Appointment:
        """
        Schedules appointment with automatic doctor selection 
        based on workload optimization.
        
        Args:
            patient_id: Patient's unique ID
            specialty: Required doctor specialty
            room_id: Room's unique ID
            date: Appointment date (YYYY-MM-DD)
            time: Appointment time (HH:MM)
            reason: Reason for appointment
            
        Returns:
            Created Appointment object
            
        Raises:
            PatientNotFoundError: Patient doesn't exist
            DoctorNotFoundError: No doctors with specialty
            RoomNotFoundError: Room doesn't exist
            AppointmentConflictError: Doctor or room not available
            InvalidAppointmentError: Invalid data
        """
        # Validate
        if not date or not time or not reason:
            raise InvalidAppointmentError("Date, time, and reason required")
        
        # Find patient
        patient = self.find_patient_by_id(patient_id)
        if not patient:
            raise PatientNotFoundError(patient_id)
        
        # Find room
        room = self.find_room_by_id(room_id)
        if not room:
            from .exceptions import RoomNotFoundError
            raise RoomNotFoundError(room_id)
        
        # Find least busy doctor in specialty (OPTIMIZATION)
        doctor = self.find_least_busy_doctor(specialty)
        if not doctor:
            raise DoctorNotFoundError(f"No doctors found with specialty: {specialty}")
        
        # Check doctor availability
        if not doctor.is_available(date, time):
            raise AppointmentConflictError(date, time, doctor.name)
        
        # Check room availability
        if not room.is_available(date, time):
            raise AppointmentConflictError(date, time, f"Room {room.room_number}")
        
        # Create appointment with room
        appointment = Appointment(date, time, reason, patient, doctor, room)
        
        # Update doctor's schedule
        doctor.add_appointment(date, time)
        
        # Update room's schedule
        room.add_reservation(date, time)
        
        # Register appointment
        self._appointments[appointment.get_id()] = appointment
        
        return appointment
    
    # ==================== APPOINTMENT SCHEDULING ====================
    
    def schedule_appointment(
        self,
        patient_id: str,
        doctor_id: str,
        room_id: str,
        date: str,
        time: str,
        reason: str
    ) -> Appointment:
        """
        Schedules appointment with specific doctor and room.
        
        Args:
            patient_id: Patient's unique ID
            doctor_id: Doctor's staff ID
            room_id: Room's unique ID
            date: Appointment date (YYYY-MM-DD)
            time: Appointment time (HH:MM)
            reason: Reason for appointment
            
        Returns:
            Created Appointment object
            
        Raises:
            PatientNotFoundError: Patient doesn't exist
            DoctorNotFoundError: Doctor doesn't exist
            RoomNotFoundError: Room doesn't exist
            AppointmentConflictError: Doctor or room not available
            InvalidAppointmentError: Invalid data
        """
        # Validate
        if not date or not time or not reason:
            raise InvalidAppointmentError("Date, time, and reason required")
        
        # Find patient
        patient = self.find_patient_by_id(patient_id)
        if not patient:
            raise PatientNotFoundError(patient_id)
        
        # Find doctor
        doctor = self.find_doctor_by_id(doctor_id)
        if not doctor:
            raise DoctorNotFoundError(doctor_id)
        
        # Find room
        room = self.find_room_by_id(room_id)
        if not room:
            from .exceptions import RoomNotFoundError
            raise RoomNotFoundError(room_id)
        
        # Check doctor availability
        if not doctor.is_available(date, time):
            raise AppointmentConflictError(date, time, doctor.name)
        
        # Check room availability
        if not room.is_available(date, time):
            raise AppointmentConflictError(date, time, f"Room {room.room_number}")
        
        # Create appointment with room
        appointment = Appointment(date, time, reason, patient, doctor, room)
        
        # Update doctor's schedule
        doctor.add_appointment(date, time)
        
        # Update room's schedule
        room.add_reservation(date, time)
        
        # Register appointment
        self._appointments[appointment.get_id()] = appointment
        
        return appointment
    
    def cancel_appointment(self, appointment_id: str) -> None:
        """
        Cancels an appointment and frees doctor's and room's schedule.
        
        Args:
            appointment_id: Unique appointment identifier
            
        Raises:
            InvalidAppointmentError: Appointment doesn't exist
        """
        appointment = self._appointments.get(appointment_id)
        if not appointment:
            raise InvalidAppointmentError(f"Appointment not found")
        
        # Mark as cancelled
        appointment.cancel()
        
        # Free up doctor's schedule
        appointment.doctor.remove_appointment(appointment.date, appointment.time)
        
        # Free up room's schedule
        appointment.room.remove_reservation(appointment.date, appointment.time)
    
    # ==================== STAGE 3: STATISTICAL REPORTING ====================
    
    def get_doctor_workload_report(self) -> Dict[str, Dict[str, any]]:
        """
        Generates workload report for all doctors.
        
        Returns:
            Dictionary with doctor statistics:
            {
                "doctor_id": {
                    "name": "Dr. Name",
                    "specialty": "Specialty",
                    "total_appointments": int,
                    "active_appointments": int,
                    "cancelled_appointments": int,
                    "occupancy_rate": float (0-100)
                }
            }
        """
        report = {}
        
        for doctor in self._doctors.values():
            doctor_id = doctor.get_id()
            
            # Get all appointments for this doctor
            doctor_appointments = [
                appt for appt in self._appointments.values()
                if appt.doctor.get_id() == doctor_id
            ]
            
            total = len(doctor_appointments)
            active = sum(1 for appt in doctor_appointments if appt.status == "scheduled")
            cancelled = sum(1 for appt in doctor_appointments if appt.status == "cancelled")
            
            # Calculate occupancy rate (assuming 40 slots per week as 100%)
            max_capacity = 40  # configurable
            occupancy_rate = (active / max_capacity * 100) if max_capacity > 0 else 0
            
            report[doctor_id] = {
                "name": doctor.name,
                "specialty": doctor.specialty,
                "total_appointments": total,
                "active_appointments": active,
                "cancelled_appointments": cancelled,
                "occupancy_rate": round(occupancy_rate, 2)
            }
        
        return report
    
    def get_room_occupancy_report(self) -> Dict[str, Dict[str, any]]:
        """
        Generates occupancy report for all rooms.
        
        Returns:
            Dictionary with room statistics:
            {
                "room_id": {
                    "room_number": int,
                    "type": "Room Type",
                    "capacity": int,
                    "total_reservations": int,
                    "occupancy_rate": float (0-100)
                }
            }
        """
        report = {}
        
        for room in self._rooms.values():
            room_id = room.get_id()
            
            # Count reservations (from room's internal tracking)
            # Since Room class doesn't track appointments in Stage 2,
            # we calculate based on theoretical capacity
            total_reservations = len(getattr(room, '_reservations', []))
            
            # Calculate occupancy (assuming 168 hours per week as 100%)
            max_hours = 168  # 24h * 7 days
            occupancy_rate = (total_reservations / max_hours * 100) if max_hours > 0 else 0
            
            report[room_id] = {
                "room_number": room.room_number,
                "type": room.type,
                "capacity": room.capacity,
                "total_reservations": total_reservations,
                "occupancy_rate": round(occupancy_rate, 2)
            }
        
        return report
    
    def get_specialty_report(self) -> Dict[str, Dict[str, int]]:
        """
        Generates report grouped by medical specialty.
        
        Returns:
            Dictionary with specialty statistics:
            {
                "specialty_name": {
                    "doctor_count": int,
                    "total_appointments": int,
                    "active_appointments": int,
                    "cancelled_appointments": int
                }
            }
        """
        report = {}
        
        # Get all unique specialties
        specialties = set(doctor.specialty for doctor in self._doctors.values())
        
        for specialty in specialties:
            # Get doctors in this specialty
            specialty_doctors = self.find_doctor_by_specialty(specialty)
            doctor_ids = [d.get_id() for d in specialty_doctors]
            
            # Get appointments for these doctors
            specialty_appointments = [
                appt for appt in self._appointments.values()
                if appt.doctor.get_id() in doctor_ids
            ]
            
            total = len(specialty_appointments)
            active = sum(1 for appt in specialty_appointments if appt.status == "scheduled")
            cancelled = sum(1 for appt in specialty_appointments if appt.status == "cancelled")
            
            report[specialty] = {
                "doctor_count": len(specialty_doctors),
                "total_appointments": total,
                "active_appointments": active,
                "cancelled_appointments": cancelled
            }
        
        return report
    
    def get_overall_statistics(self) -> Dict[str, any]:
        """
        Generates overall hospital statistics.
        
        Returns:
            Dictionary with overall metrics:
            {
                "total_patients": int,
                "total_doctors": int,
                "total_rooms": int,
                "total_appointments": int,
                "active_appointments": int,
                "cancelled_appointments": int,
                "cancellation_rate": float (0-100)
            }
        """
        total_appts = len(self._appointments)
        active = sum(1 for appt in self._appointments.values() if appt.status == "scheduled")
        cancelled = sum(1 for appt in self._appointments.values() if appt.status == "cancelled")
        
        cancellation_rate = (cancelled / total_appts * 100) if total_appts > 0 else 0
        
        return {
            "total_patients": len(self._patients),
            "total_doctors": len(self._doctors),
            "total_rooms": len(self._rooms),
            "total_appointments": total_appts,
            "active_appointments": active,
            "cancelled_appointments": cancelled,
            "cancellation_rate": round(cancellation_rate, 2)
        }
    
    # ==================== BASIC STATISTICS (Stage 2) ====================
    
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
                f"Appointments: {self.get_active_appointments()}>")