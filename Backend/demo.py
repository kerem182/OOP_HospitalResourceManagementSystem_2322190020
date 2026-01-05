"""
Demo script for Stage 3 features.
Demonstrates workload optimization and statistical reporting.
"""
from app.hospital import Hospital
from app.patient import Patient
from app.doctor import Doctor
from app.room import Room
import json


def print_section(title: str):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def main():
    """Demo Stage 3 features."""
    
    print_section("STAGE 3: ADVANCED ALGORITHMS & REPORTING DEMO")
    
    # Create hospital
    hospital = Hospital("Istanbul Medical Center")
    print(f"\n✓ Created: {hospital}")
    
    # ==================== SETUP DATA ====================
    print_section("1. SETTING UP TEST DATA")
    
    # Register patients
    patients = [
        Patient("Kerem Salih Erol", "P001", "2005-02-18"),
        Patient("Ayşe Yılmaz", "P002", "1992-05-10"),
        Patient("Mehmet Kaya", "P003", "1985-11-22"),
        Patient("Fatma Demir", "P004", "1995-07-15"),
        Patient("Ali Çelik", "P005", "1988-03-30"),
    ]
    
    for patient in patients:
        hospital.register_patient(patient)
    print(f"✓ Registered {len(patients)} patients")
    
    # Register doctors (multiple in same specialty)
    doctors = [
        Doctor("Dr. Coşkun Şahin", "D001", "Cardiology"),
        Doctor("Dr. Ayşe Demir", "D002", "Cardiology"),  # Another cardiologist
        Doctor("Dr. Mehmet Öztürk", "D003", "Neurology"),
        Doctor("Dr. Zeynep Yıldız", "D004", "Orthopedics"),
    ]
    
    for doctor in doctors:
        hospital.register_doctor(doctor)
    print(f"✓ Registered {len(doctors)} doctors")
    print("   - 2 Cardiologists (for workload balancing demo)")
    print("   - 1 Neurologist")
    print("   - 1 Orthopedist")
    
    # Register rooms
    rooms = [
        Room(101, 1, "Surgery Room"),
        Room(102, 2, "ICU"),
        Room(103, 4, "Standard Ward"),
    ]
    
    for room in rooms:
        hospital.register_room(room)
    print(f"✓ Registered {len(rooms)} rooms")
    
    # ==================== WORKLOAD OPTIMIZATION ====================
    print_section("2. WORKLOAD OPTIMIZATION ALGORITHM")
    
    print("\n📊 Initial State: All cardiologists have 0 appointments")
    
    # Give Dr. Coşkun Şahin some appointments
    print("\n📅 Manually scheduling 3 appointments with Dr. Coşkun Şahin:")
    hospital.schedule_appointment("P001", "D001", "101", "2025-12-20", "09:00", "Checkup")
    hospital.schedule_appointment("P002", "D001", "102", "2025-12-20", "10:00", "Follow-up")
    hospital.schedule_appointment("P003", "D001", "103", "2025-12-20", "11:00", "Consultation")
    print("   ✓ Dr. Coşkun Şahin now has 3 appointments")
    
    # Dr. Ayşe Demir has 0 appointments
    print("   ✓ Dr. Ayşe Demir has 0 appointments")
    
    print("\n🔍 Finding least busy cardiologist:")
    least_busy = hospital.find_least_busy_doctor("Cardiology")
    print(f"   → Result: {least_busy.name} (ID: {least_busy.get_id()})")
    print(f"   → This doctor has the fewest active appointments")
    
    print("\n🎯 Using optimized scheduling (auto-selects least busy doctor):")
    try:
        appointment = hospital.schedule_appointment_optimized(
            patient_id="P004",
            specialty="Cardiology",
            room_id="101",
            date="2025-12-21",
            time="09:00",
            reason="Cardiac assessment"
        )
        print(f"   ✓ Patient P004 automatically assigned to: {appointment.doctor.name}")
        print(f"   ✓ Algorithm chose the doctor with least workload")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Add one more appointment to test balancing again
    appointment2 = hospital.schedule_appointment_optimized(
        patient_id="P005",
        specialty="Cardiology",
        room_id="102",
        date="2025-12-21",
        time="10:00",
        reason="Heart monitoring"
    )
    print(f"   ✓ Patient P005 assigned to: {appointment2.doctor.name}")
    
    # ==================== STATISTICAL REPORTING ====================
    print_section("3. STATISTICAL REPORTING")
    
    # Cancel one appointment for statistics demo
    hospital.cancel_appointment("2025-12-20_10:00_P002")
    print("\n📝 Note: Cancelled one appointment for statistics demo\n")
    
    # Doctor Workload Report
    print("📊 DOCTOR WORKLOAD REPORT")
    print("-" * 70)
    workload_report = hospital.get_doctor_workload_report()
    
    for doctor_id, data in workload_report.items():
        print(f"\n{data['name']} ({data['specialty']})")
        print(f"  Total Appointments:     {data['total_appointments']}")
        print(f"  Active Appointments:    {data['active_appointments']}")
        print(f"  Cancelled Appointments: {data['cancelled_appointments']}")
        print(f"  Occupancy Rate:         {data['occupancy_rate']}%")
    
    # Room Occupancy Report
    print("\n\n🏥 ROOM OCCUPANCY REPORT")
    print("-" * 70)
    room_report = hospital.get_room_occupancy_report()
    
    for room_id, data in room_report.items():
        print(f"\nRoom {data['room_number']} ({data['type']})")
        print(f"  Capacity:          {data['capacity']} patients")
        print(f"  Total Reservations: {data['total_reservations']}")
        print(f"  Occupancy Rate:    {data['occupancy_rate']}%")
    
    # Specialty Report
    print("\n\n🏥 SPECIALTY-BASED REPORT")
    print("-" * 70)
    specialty_report = hospital.get_specialty_report()
    
    for specialty, data in specialty_report.items():
        print(f"\n{specialty}")
        print(f"  Doctors:                {data['doctor_count']}")
        print(f"  Total Appointments:     {data['total_appointments']}")
        print(f"  Active Appointments:    {data['active_appointments']}")
        print(f"  Cancelled Appointments: {data['cancelled_appointments']}")
    
    # Overall Statistics
    print("\n\n📈 OVERALL HOSPITAL STATISTICS")
    print("-" * 70)
    overall_stats = hospital.get_overall_statistics()
    
    print(f"\nResources:")
    print(f"  Total Patients:         {overall_stats['total_patients']}")
    print(f"  Total Doctors:          {overall_stats['total_doctors']}")
    print(f"  Total Rooms:            {overall_stats['total_rooms']}")
    
    print(f"\nAppointments:")
    print(f"  Total Appointments:     {overall_stats['total_appointments']}")
    print(f"  Active Appointments:    {overall_stats['active_appointments']}")
    print(f"  Cancelled Appointments: {overall_stats['cancelled_appointments']}")
    print(f"  Cancellation Rate:      {overall_stats['cancellation_rate']}%")
    
    # ==================== JSON EXPORT (for web integration) ====================
    print_section("4. JSON DATA EXPORT (for Web Integration)")
    
    print("\n📤 Exporting reports as JSON (ready for Flask/Streamlit):\n")
    
    # Export all reports
    reports = {
        "workload": workload_report,
        "rooms": room_report,
        "specialties": specialty_report,
        "overall": overall_stats
    }
    
    print(json.dumps(reports, indent=2))
    
    print_section("✓ STAGE 3 DEMO COMPLETED")
    print("\n💡 These methods are ready to be integrated with web framework:")
    print("   - hospital.find_least_busy_doctor(specialty)")
    print("   - hospital.schedule_appointment_optimized(...)")
    print("   - hospital.get_doctor_workload_report()")
    print("   - hospital.get_room_occupancy_report()")
    print("   - hospital.get_specialty_report()")
    print("   - hospital.get_overall_statistics()")
    print()


if __name__ == "__main__":
    main()