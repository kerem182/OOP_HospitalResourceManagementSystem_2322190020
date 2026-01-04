"""
Hospital Resource Management System - Web Interface
Streamlit application for managing hospital appointments and viewing statistics.
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from app.hospital import Hospital
from app.patient import Patient
from app.doctor import Doctor
from app.room import Room
from app.exceptions import (
    PatientNotFoundError,
    DoctorNotFoundError,
    RoomNotFoundError,
    AppointmentConflictError,
    InvalidAppointmentError
)


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== SESSION STATE INITIALIZATION ====================

def initialize_session_state():
    """Initialize session state with hospital and sample data."""
    if 'hospital' not in st.session_state:
        # Create hospital instance
        st.session_state.hospital = Hospital("Istanbul Medical Center")
        
        # Add sample patients
        sample_patients = [
            Patient("Kerem Salih Erol", "P001", "2005-02-18"),
            Patient("Ayşe Yılmaz", "P002", "1992-05-10"),
            Patient("Mehmet Kaya", "P003", "1985-11-22"),
            Patient("Fatma Demir", "P004", "1995-07-15"),
            Patient("Ali Çelik", "P005", "1988-03-30"),
        ]
        
        for patient in sample_patients:
            st.session_state.hospital.register_patient(patient)
        
        # Add sample doctors
        sample_doctors = [
            Doctor("Dr. Coşkun Şahin", "D001", "Cardiology"),
            Doctor("Dr. Ayşe Demir", "D002", "Cardiology"),
            Doctor("Dr. Mehmet Öztürk", "D003", "Neurology"),
            Doctor("Dr. Zeynep Yıldız", "D004", "Orthopedics"),
            Doctor("Dr. Ahmet Kaya", "D005", "Pediatrics"),
        ]
        
        for doctor in sample_doctors:
            st.session_state.hospital.register_doctor(doctor)
        
        # Add sample rooms
        sample_rooms = [
            Room(101, 1, "Consultation Room"),
            Room(102, 2, "ICU"),
            Room(103, 1, "Surgery Room"),
            Room(104, 4, "Standard Ward"),
            Room(105, 1, "Examination Room"),
        ]
        
        for room in sample_rooms:
            st.session_state.hospital.register_room(room)


# ==================== HELPER FUNCTIONS ====================

def get_hospital():
    """Get hospital instance from session state."""
    return st.session_state.hospital


def format_date(date_str):
    """Format date string for display."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str


def get_available_specialties():
    """Get list of unique specialties."""
    hospital = get_hospital()
    specialties = set()
    for doctor in hospital._doctors.values():
        specialties.add(doctor.specialty)
    return sorted(list(specialties))


def get_patient_list():
    """Get list of patients for dropdown."""
    hospital = get_hospital()
    return {f"{p.name} ({p.patient_id})": p.patient_id 
            for p in hospital._patients.values()}


# ==================== DASHBOARD METRICS ====================

def show_dashboard_metrics():
    """Display key hospital statistics at the top."""
    st.title("🏥 Hospital Management Dashboard")
    st.markdown("---")
    
    hospital = get_hospital()
    stats = hospital.get_overall_statistics()
    
    # Create 4 columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Patients",
            value=stats['total_patients'],
            delta=None
        )
    
    with col2:
        st.metric(
            label="👨‍⚕️ Total Doctors",
            value=stats['total_doctors'],
            delta=None
        )
    
    with col3:
        st.metric(
            label="📅 Active Appointments",
            value=stats['active_appointments'],
            delta=None
        )
    
    with col4:
        cancellation_rate = stats['cancellation_rate']
        st.metric(
            label="❌ Cancellation Rate",
            value=f"{cancellation_rate:.1f}%",
            delta=f"{cancellation_rate:.1f}%" if cancellation_rate > 0 else "0%",
            delta_color="inverse"
        )


# ==================== VISUAL REPORTING ====================

def show_visual_reports():
    """Display visual reports with charts."""
    st.header("📊 Visual Analytics")
    
    hospital = get_hospital()
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Doctor Workload")
        workload_report = hospital.get_doctor_workload_report()
        
        if workload_report:
            # Prepare data for chart
            doctor_names = []
            active_counts = []
            
            for doctor_id, data in workload_report.items():
                doctor_names.append(data['name'])
                active_counts.append(data['active_appointments'])
            
            # Create DataFrame
            df_workload = pd.DataFrame({
                'Doctor': doctor_names,
                'Active Appointments': active_counts
            })
            
            # Display bar chart
            st.bar_chart(df_workload.set_index('Doctor'))
            
            # Display detailed table
            with st.expander("📋 View Detailed Workload Data"):
                detailed_data = []
                for doctor_id, data in workload_report.items():
                    detailed_data.append({
                        'Doctor': data['name'],
                        'Specialty': data['specialty'],
                        'Total': data['total_appointments'],
                        'Active': data['active_appointments'],
                        'Cancelled': data['cancelled_appointments'],
                        'Occupancy': f"{data['occupancy_rate']:.1f}%"
                    })
                st.dataframe(pd.DataFrame(detailed_data), use_container_width=True)
        else:
            st.info("No doctor workload data available.")
    
    with col2:
        st.subheader("Room Occupancy")
        room_report = hospital.get_room_occupancy_report()
        
        if room_report:
            # Prepare data for chart
            room_names = []
            occupancy_rates = []
            
            for room_id, data in room_report.items():
                room_names.append(f"Room {data['room_number']}")
                occupancy_rates.append(data['occupancy_rate'])
            
            # Create DataFrame
            df_rooms = pd.DataFrame({
                'Room': room_names,
                'Occupancy Rate (%)': occupancy_rates
            })
            
            # Display bar chart
            st.bar_chart(df_rooms.set_index('Room'))
            
            # Display detailed table
            with st.expander("📋 View Detailed Room Data"):
                detailed_data = []
                for room_id, data in room_report.items():
                    detailed_data.append({
                        'Room': data['room_number'],
                        'Type': data['type'],
                        'Capacity': data['capacity'],
                        'Reservations': data['total_reservations'],
                        'Occupancy': f"{data['occupancy_rate']:.1f}%"
                    })
                st.dataframe(pd.DataFrame(detailed_data), use_container_width=True)
        else:
            st.info("No room occupancy data available.")


# ==================== SPECIALTY REPORT ====================

def show_specialty_report():
    """Display specialty-based statistics."""
    st.header("🏥 Specialty Statistics")
    
    hospital = get_hospital()
    specialty_report = hospital.get_specialty_report()
    
    if specialty_report:
        # Prepare data
        specialty_data = []
        for specialty, data in specialty_report.items():
            specialty_data.append({
                'Specialty': specialty,
                'Doctors': data['doctor_count'],
                'Total Appointments': data['total_appointments'],
                'Active': data['active_appointments'],
                'Cancelled': data['cancelled_appointments']
            })
        
        df_specialty = pd.DataFrame(specialty_data)
        st.dataframe(df_specialty, use_container_width=True, hide_index=True)
    else:
        st.info("No specialty data available.")


# ==================== SMART APPOINTMENT FORM ====================

def show_appointment_form():
    """Display smart appointment booking form with optimization."""
    st.header("📅 Smart Appointment Booking")
    st.markdown("**System automatically assigns the least busy doctor in selected specialty**")
    
    hospital = get_hospital()
    
    with st.form("appointment_form"):
        # Patient selection
        patient_dict = get_patient_list()
        selected_patient = st.selectbox(
            "Select Patient",
            options=list(patient_dict.keys()),
            help="Choose patient from registered list"
        )
        
        # Specialty selection
        specialties = get_available_specialties()
        selected_specialty = st.selectbox(
            "Select Specialty",
            options=specialties,
            help="System will automatically select the least busy doctor"
        )
        
        # Room selection
        room_options = {f"Room {r.room_number} ({r.type})": r.get_id() 
                       for r in hospital._rooms.values()}
        selected_room = st.selectbox(
            "Select Room",
            options=list(room_options.keys()),
            help="Choose examination room"
        )
        
        # Date and time
        col1, col2 = st.columns(2)
        
        with col1:
            appointment_date = st.date_input(
                "Appointment Date",
                value=datetime.now() + timedelta(days=1),
                min_value=datetime.now(),
                help="Select future date"
            )
        
        with col2:
            time_slots = [f"{h:02d}:00" for h in range(9, 17)]  # 09:00 to 16:00
            appointment_time = st.selectbox(
                "Appointment Time",
                options=time_slots,
                help="Available time slots"
            )
        
        # Reason
        reason = st.text_area(
            "Reason for Visit",
            placeholder="Enter reason for appointment...",
            help="Brief description of the medical issue"
        )
        
        # Submit button
        submitted = st.form_submit_button("🎯 Book Appointment (Smart Assignment)", 
                                         use_container_width=True)
        
        if submitted:
            if not reason.strip():
                st.error("❌ Please provide a reason for the visit.")
            else:
                try:
                    # Get IDs
                    patient_id = patient_dict[selected_patient]
                    room_id = room_options[selected_room]
                    date_str = appointment_date.strftime("%Y-%m-%d")
                    
                    # Create optimized appointment
                    appointment = hospital.schedule_appointment_optimized(
                        patient_id=patient_id,
                        specialty=selected_specialty,
                        room_id=room_id,
                        date=date_str,
                        time=appointment_time,
                        reason=reason.strip()
                    )
                    
                    # Success message
                    st.success(f"""
                    ✅ **Appointment Booked Successfully!**
                    
                    - **Patient:** {appointment.patient.name}
                    - **Doctor:** {appointment.doctor.name} ({appointment.doctor.specialty})
                    - **Date:** {format_date(appointment.date)}
                    - **Time:** {appointment.time}
                    - **Room:** {selected_room}
                    
                    *Doctor was automatically selected based on current workload.*
                    """)
                    
                    # Show which doctor was selected
                    st.info(f"🎯 **Smart Assignment:** System selected {appointment.doctor.name} "
                           f"(least busy {selected_specialty} specialist)")
                    
                except AppointmentConflictError as e:
                    st.error(f"❌ **Scheduling Conflict:** {str(e)}")
                    st.info("💡 Try selecting a different time slot or room.")
                    
                except (PatientNotFoundError, DoctorNotFoundError, RoomNotFoundError) as e:
                    st.error(f"❌ **Error:** {str(e)}")
                    
                except InvalidAppointmentError as e:
                    st.error(f"❌ **Invalid Data:** {str(e)}")
                    
                except Exception as e:
                    st.error(f"❌ **Unexpected Error:** {str(e)}")


# ==================== APPOINTMENT LIST ====================

def show_appointments_list():
    """Display list of all appointments."""
    st.header("📋 Appointment List")
    
    hospital = get_hospital()
    
    if hospital._appointments:
        # Prepare data
        appointment_data = []
        for appt in hospital._appointments.values():
            appointment_data.append({
                'ID': appt.get_id(),
                'Patient': appt.patient.name,
                'Doctor': appt.doctor.name,
                'Specialty': appt.doctor.specialty,
                'Date': appt.date,
                'Time': appt.time,
                'Reason': appt.reason,
                'Status': appt.status.upper()
            })
        
        df_appointments = pd.DataFrame(appointment_data)
        
        # Filter by status
        status_filter = st.radio(
            "Filter by Status:",
            options=["All", "Scheduled", "Cancelled"],
            horizontal=True
        )
        
        if status_filter == "Scheduled":
            df_filtered = df_appointments[df_appointments['Status'] == 'SCHEDULED']
        elif status_filter == "Cancelled":
            df_filtered = df_appointments[df_appointments['Status'] == 'CANCELLED']
        else:
            df_filtered = df_appointments
        
        # Display table
        st.dataframe(
            df_filtered,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Appointment status"
                )
            }
        )
        
        st.caption(f"Total: {len(df_filtered)} appointments")

        # === CANCELLATION PROCESS STARTS HERE ===
        st.markdown("---")
        st.subheader("❌ Appointment Cancellation Panel")
        
        # Only offers active (Scheduled) appointments for selection
        active_appts = [appt.get_id() for appt in hospital._appointments.values() if appt.status == "scheduled"]
        
        if active_appts:
            selected_id = st.selectbox("Select the Appointment ID you want to cancel:", options=active_appts)
            
            if st.button("Cancel Selected Appointment", use_container_width=True, type="primary"):
                try:
                    hospital.cancel_appointment(selected_id) # Calls the Backend method
                    st.success(f"✅ Appointment ID {selected_id} has been successfully cancelled and resources have been released.")
                    st.rerun() # Refreshes the page to update charts and the list
                except Exception as e:
                    st.error(f"An error occurred during the cancellation process: {e}")
        else:
            st.info("There are no active appointments available for cancellation.")
        
    else:
        st.info("📭 No appointments scheduled yet. Use the form above to create one!")


# ==================== SIDEBAR ====================

def show_sidebar():
    """Display sidebar with additional options."""
    with st.sidebar:
        st.title("🏥 Hospital System")
        st.markdown("---")
        
        st.subheader("📊 Quick Stats")
        hospital = get_hospital()
        stats = hospital.get_overall_statistics()
        
        st.metric("Total Appointments", stats['total_appointments'])
        st.metric("Active", stats['active_appointments'])
        st.metric("Cancelled", stats['cancelled_appointments'])
        
        st.markdown("---")
        
        st.subheader("ℹ️ About")
        st.info("""
        **Hospital Resource Management System**
        
        Stage 3: Advanced Implementation
        
        Features:
        - Smart appointment booking
        - Workload optimization
        - Real-time analytics
        - Visual reporting
        """)
        
        st.markdown("---")
        
        # Data management
        st.subheader("🔧 Data Management")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        if st.button("🗑️ Clear All Appointments", use_container_width=True):
            if st.session_state.hospital._appointments:
                st.session_state.hospital._appointments.clear()
                st.success("All appointments cleared!")
                st.rerun()
        
        st.markdown("---")
        st.caption("© 2024 Hospital Management System")


# ==================== MAIN APPLICATION ====================

def main():
    """Main application entry point."""
    # Initialize session state
    initialize_session_state()
    
    # Show sidebar
    show_sidebar()
    
    # Main content
    show_dashboard_metrics()
    
    st.markdown("---")
    
    # Visual reports
    show_visual_reports()
    
    st.markdown("---")
    
    # Specialty report
    show_specialty_report()
    
    st.markdown("---")
    
    # Appointment form
    show_appointment_form()
    
    st.markdown("---")
    
    # Appointments list
    show_appointments_list()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>Hospital Resource Management System | Stage 3: Web Implementation</p>
        <p>Built with Streamlit 🎈 | Powered by Python 🐍</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()