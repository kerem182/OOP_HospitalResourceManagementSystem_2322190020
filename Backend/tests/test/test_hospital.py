"""
Unit tests for Hospital Resource Management System.
Stage 2: Essential tests covering core functionality.
"""

import unittest
from unittest.mock import Mock
from app.patient import Patient
from app.doctor import Doctor
from app.appointment import Appointment
from app.hospital import Hospital
from app.hospital import Room
from app.exceptions import (
    PatientNotFoundError,
    DoctorNotFoundError,
    AppointmentConflictError,
    InvalidAppointmentError
)


class TestDoctor(unittest.TestCase):
    """Tests for Doctor scheduling functionality."""
    
    def test_doctor_availability(self):
        """Test doctor availability checking."""
        doctor = Doctor("Dr. Smith", "D001", "Cardiology")
        
        # Initially available
        self.assertTrue(doctor.is_available("2025-12-20", "09:00"))
        
        # Add appointment
        doctor.add_appointment("2025-12-20", "09:00")
        
        # Now not available
        self.assertFalse(doctor.is_available("2025-12-20", "09:00"))


class TestAppointment(unittest.TestCase):
    """Tests for Appointment composition."""
    
    def test_appointment_composition(self):
        """Test that appointment contains patient and doctor."""
        patient = Patient("John Doe", "P001", "1990-01-01")
        doctor = Doctor("Dr. Smith", "D001", "Cardiology")
        room = Room(101, 1, "Consultation Room")
        appointment = Appointment("2025-12-20", "09:00", "Checkup", patient, doctor, room)

        
        # Verify composition
        self.assertEqual(appointment.patient, patient)
        self.assertEqual(appointment.doctor, doctor)
        self.assertEqual(appointment.status, "scheduled")


class TestHospital(unittest.TestCase):
    """Tests for Hospital coordinator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.hospital = Hospital("Test Hospital")
        self.patient = Patient("John Doe", "P001", "1990-01-01")
        self.doctor = Doctor("Dr. Smith", "D001", "Cardiology")
        self.room = Room(101, 2, "Consultation Room") 
        self.hospital.register_room(self.room)        
    
    def test_register_patient(self):
        """Test patient registration."""
        self.hospital.register_patient(self.patient)
        found = self.hospital.find_patient_by_id("P001")
        self.assertEqual(found, self.patient)
    
    def test_register_doctor(self):
        """Test doctor registration."""
        self.hospital.register_doctor(self.doctor)
        found = self.hospital.find_doctor_by_id("D001")
        self.assertEqual(found, self.doctor)
    
    def test_search_by_specialty(self):
        """Test search algorithm by specialty."""
        self.hospital.register_doctor(self.doctor)
        doctor2 = Doctor("Dr. Jones", "D002", "Neurology")
        self.hospital.register_doctor(doctor2)
        
        cardiologists = self.hospital.find_doctor_by_specialty("Cardiology")
        self.assertEqual(len(cardiologists), 1)
        self.assertEqual(cardiologists[0].staff_id, "D001")
    
    def test_schedule_appointment_success(self):
        """Test successful appointment scheduling."""
        self.hospital.register_patient(self.patient)
        self.hospital.register_doctor(self.doctor)
        
        appointment = self.hospital.schedule_appointment(
        patient_id="P001",
        doctor_id="D001",
        room_id="101",
        date="2025-12-20",
        time="09:00",
        reason="Routine checkup"
        )
        
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.patient, self.patient)
        self.assertEqual(self.hospital.get_active_appointments(), 1)
    
    def test_patient_not_found_error(self):
        """Test PatientNotFoundError exception."""
        self.hospital.register_doctor(self.doctor)
        
        with self.assertRaises(PatientNotFoundError):
            self.hospital.schedule_appointment(
                patient_id="P999",
                doctor_id="D001",
                room_id="101",
                date="2025-12-20",
                time="09:00",
                reason="Test"
            )
    
    def test_doctor_not_found_error(self):
        """Test DoctorNotFoundError exception."""
        self.hospital.register_patient(self.patient)
        
        with self.assertRaises(DoctorNotFoundError):
            self.hospital.schedule_appointment(
                patient_id="P001",
                doctor_id="D999",
                room_id="101",
                date="2025-12-20",
                time="09:00",
                reason="Checkup"
            )
    
    def test_appointment_conflict_error(self):
        """Test AppointmentConflictError exception."""
        self.hospital.register_patient(self.patient)
        self.hospital.register_doctor(self.doctor)
    
        patient2 = Patient("Jane Doe", "P002", "1992-05-15")
        self.hospital.register_patient(patient2)

    # Schedule first appointment
        self.hospital.schedule_appointment(
        "P001", "D001", "101", "2025-12-20", "09:00", "Checkup"
    )

    # Try to schedule at same time - should raise error   
        with self.assertRaises(AppointmentConflictError):
         self.hospital.schedule_appointment(
            "P002", "D001", "101", "2025-12-20", "09:00", "Checkup"
        )

    
    def test_cancel_appointment(self):
        """Test appointment cancellation."""
        self.hospital.register_patient(self.patient)
        self.hospital.register_doctor(self.doctor)
        
        appointment = self.hospital.schedule_appointment(
            "P001", "D001", "101", "2025-12-20", "09:00", "Checkup"
        )
        
        # Cancel
        self.hospital.cancel_appointment(appointment.get_id())
        
        # Verify cancelled
        self.assertEqual(appointment.status, "cancelled")
        self.assertEqual(self.hospital.get_active_appointments(), 0)
        
        # Verify doctor available again
        self.assertTrue(self.doctor.is_available("2025-12-20", "09:00"))
    
    def test_mock_example(self):
        """Test using mock for dependency injection."""
        hospital = Hospital("Test Hospital")
        
        local_room = Room(101, 2, "Consultation Room")
        hospital.register_room(local_room)

        # Create mock patient
        mock_patient = Mock(spec=Patient)
        mock_patient.get_id.return_value = "P001"
        
        # Real doctor
        doctor = Doctor("Dr. Smith", "D001", "Cardiology")
        hospital.register_doctor(doctor)
        
        # Inject mock
        hospital._patients["P001"] = mock_patient
        
        # Schedule
        appointment = hospital.schedule_appointment(
            "P001", "D001", "101", "2025-12-20", "09:00", "Test"
        )
        
        # Verify mock was used
        self.assertEqual(appointment.patient, mock_patient)
        mock_patient.get_id.assert_called()


if __name__ == "__main__":
    unittest.main()
