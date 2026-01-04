"""
Unit tests for Stage 3 features.
Tests workload optimization and statistical reporting.
"""
import unittest
from unittest.mock import Mock
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.room import Room
from app.models.appointment import Appointment
from app.models.hospital import Hospital
from app.models.exceptions import (
    PatientNotFoundError,
    DoctorNotFoundError,
    AppointmentConflictError,
    InvalidAppointmentError
)


class TestWorkloadOptimization(unittest.TestCase):
    """Tests for workload balancing algorithm."""
    
    def setUp(self):
        """Set up test hospital with multiple doctors."""
        self.hospital = Hospital("Test Hospital")
        
        # Register patients
        self.patient1 = Patient("John Doe", "P001", "1990-01-01")
        self.patient2 = Patient("Jane Smith", "P002", "1992-05-15")
        self.patient3 = Patient("Bob Wilson", "P003", "1985-08-20")
        
        self.hospital.register_patient(self.patient1)
        self.hospital.register_patient(self.patient2)
        self.hospital.register_patient(self.patient3)
        
        # Register multiple cardiologists
        self.doctor1 = Doctor("Dr. Smith", "D001", "Cardiology")
        self.doctor2 = Doctor("Dr. Jones", "D002", "Cardiology")
        self.doctor3 = Doctor("Dr. Brown", "D003", "Neurology")
        
        self.hospital.register_doctor(self.doctor1)
        self.hospital.register_doctor(self.doctor2)
        self.hospital.register_doctor(self.doctor3)
        
        # Register rooms
        self.room1 = Room(101, 1, "Consultation Room")
        self.room2 = Room(102, 2, "ICU")
        
        self.hospital.register_room(self.room1)
        self.hospital.register_room(self.room2)
    
    def test_find_least_busy_doctor_empty(self):
        """Test finding least busy doctor when all are free."""
        doctor = self.hospital.find_least_busy_doctor("Cardiology")
        
        # Should return one of the cardiologists
        self.assertIsNotNone(doctor)
        self.assertEqual(doctor.specialty, "Cardiology")
    
    def test_find_least_busy_doctor_with_workload(self):
        """Test finding least busy doctor with different workloads."""
        # Give Dr. Smith 2 appointments
        self.hospital.schedule_appointment(
            "P001", "D001", "101", "2025-12-20", "09:00", "Checkup"
        )
        self.hospital.schedule_appointment(
            "P002", "D001", "101", "2025-12-20", "10:00", "Follow-up"
        )
        
        # Give Dr. Jones 1 appointment
        self.hospital.schedule_appointment(
            "P003", "D002", "102", "2025-12-20", "09:00", "Checkup"
        )
        
        # Dr. Jones should be least busy
        least_busy = self.hospital.find_least_busy_doctor("Cardiology")
        self.assertEqual(least_busy.get_id(), "D002")
    
    def test_optimized_scheduling(self):
        """Test optimized appointment scheduling."""
        # Give Dr. Smith 1 appointment
        self.hospital.schedule_appointment(
            "P001", "D001", "101", "2025-12-20", "09:00", "Checkup"
        )
        
        # Schedule with optimization (should pick Dr. Jones - no appointments)
        appointment = self.hospital.schedule_appointment_optimized(
            patient_id="P002",
            specialty="Cardiology",
            room_id="102",
            date="2025-12-20",
            time="10:00",
            reason="Routine checkup"
        )
        
        # Should be assigned to least busy doctor (D002)
        self.assertEqual(appointment.doctor.get_id(), "D002")


class TestStatisticalReporting(unittest.TestCase):
    """Tests for statistical reporting methods."""
    
    def setUp(self):
        """Set up test hospital with sample data."""
        self.hospital = Hospital("Test Hospital")
        
        # Register resources
        self.patient = Patient("John Doe", "P001", "1990-01-01")
        self.doctor1 = Doctor("Dr. Smith", "D001", "Cardiology")
        self.doctor2 = Doctor("Dr. Jones", "D002", "Neurology")
        self.room = Room(101, 2, "ICU")
        
        self.hospital.register_patient(self.patient)
        self.hospital.register_doctor(self.doctor1)
        self.hospital.register_doctor(self.doctor2)
        self.hospital.register_room(self.room)
        
        # Create appointments
        self.appt1 = self.hospital.schedule_appointment(
            "P001", "D001", "101", "2025-12-20", "09:00", "Checkup"
        )
        self.appt2 = self.hospital.schedule_appointment(
            "P001", "D001", "101", "2025-12-20", "10:00", "Follow-up"
        )
        
        # Cancel one appointment
        self.hospital.cancel_appointment(self.appt2.get_id())
    
    def test_doctor_workload_report(self):
        """Test doctor workload report generation."""
        report = self.hospital.get_doctor_workload_report()
        
        # Should have reports for both doctors
        self.assertEqual(len(report), 2)
        
        # Check Dr. Smith's report
        dr_smith_report = report["D001"]
        self.assertEqual(dr_smith_report["name"], "Dr. Smith")
        self.assertEqual(dr_smith_report["specialty"], "Cardiology")
        self.assertEqual(dr_smith_report["total_appointments"], 2)
        self.assertEqual(dr_smith_report["active_appointments"], 1)
        self.assertEqual(dr_smith_report["cancelled_appointments"], 1)
        self.assertIsInstance(dr_smith_report["occupancy_rate"], float)
        
        # Check Dr. Jones's report (no appointments)
        dr_jones_report = report["D002"]
        self.assertEqual(dr_jones_report["total_appointments"], 0)
        self.assertEqual(dr_jones_report["active_appointments"], 0)
    
    def test_room_occupancy_report(self):
        """Test room occupancy report generation."""
        report = self.hospital.get_room_occupancy_report()
        
        # Should have report for the room
        self.assertEqual(len(report), 1)
        
        room_report = report["101"]
        self.assertEqual(room_report["room_number"], 101)
        self.assertEqual(room_report["type"], "ICU")
        self.assertEqual(room_report["capacity"], 2)
        self.assertIsInstance(room_report["occupancy_rate"], float)
    
    def test_specialty_report(self):
        """Test specialty-based report."""
        report = self.hospital.get_specialty_report()
        
        # Should have reports for both specialties
        self.assertIn("Cardiology", report)
        self.assertIn("Neurology", report)
        
        # Check Cardiology report
        cardio_report = report["Cardiology"]
        self.assertEqual(cardio_report["doctor_count"], 1)
        self.assertEqual(cardio_report["total_appointments"], 2)
        self.assertEqual(cardio_report["active_appointments"], 1)
        self.assertEqual(cardio_report["cancelled_appointments"], 1)
        
        # Check Neurology report (no appointments)
        neuro_report = report["Neurology"]
        self.assertEqual(neuro_report["doctor_count"], 1)
        self.assertEqual(neuro_report["total_appointments"], 0)
    
    def test_overall_statistics(self):
        """Test overall hospital statistics."""
        stats = self.hospital.get_overall_statistics()
        
        self.assertEqual(stats["total_patients"], 1)
        self.assertEqual(stats["total_doctors"], 2)
        self.assertEqual(stats["total_rooms"], 1)
        self.assertEqual(stats["total_appointments"], 2)
        self.assertEqual(stats["active_appointments"], 1)
        self.assertEqual(stats["cancelled_appointments"], 1)
        self.assertEqual(stats["cancellation_rate"], 50.0)


if __name__ == "__main__":
    unittest.main()