import time
import pandas as pd
import notification
from user import Nurse, UserLoader, NurseFactory
from appointment import Appointment

def run_nurse_portal(nurse):
    """Runs the nurse portal after a successful login."""
    # Call login function from login.py
    if nurse:
        nurse = load_nurse_data(nurse)
        if nurse:
            assigned_patients, vitals_dict = load_patient_data_for_nurse(nurse.name)
            nurse.assigned_patients = assigned_patients
            nurse.vitals_dict = vitals_dict
        
            print(f"Welcome, User {nurse.username}!")
            time.sleep(1)
            nurse_dashboard(nurse)
        else:
            print("Error loading nurse dashboard.")

if __name__ == "__main__":
    run_nurse_portal("Carol Lee")
 

#CSV Management
def load_nurse_data(nurse):
    """Load nurse data using UserLoader."""
    nurses = UserLoader.load_users("nurse")

    # Extract the username from the nurse_username parameter
    nurse_username = nurse.username  # Assuming nurse_username is a Nurse object

    # Find nurse by name
    for nurse in nurses:
        if nurse.username == nurse_username:  # Compare with the extracted username
            return nurse
            
    print("No nurse data found for the provided username.")
    return None

def update_nurse_data(nurse):
    """Updates the nurse's information in nurse.csv using data from the Nurse object."""
    try:
        # Load the CSV
        nurses_df = pd.read_csv("nurse.csv")
        
        # Find the nurse by username
        nurse_index = nurses_df.index[nurses_df["Username"] == nurse.username].tolist()
        if not nurse_index:
            print(f"No record found for nurse {nurse.username}. Cannot update.")
            return
        
        # Update fields
        nurse_index = nurse_index[0]
        nurses_df.at[nurse_index, "AssignedPatients"] = ";".join(nurse.assigned_patients)
        nurses_df.at[nurse_index, "Availability"] = nurse.available
        nurses_df.at[nurse_index, "TriageReady"] = nurse.triage_ready
        nurses_df.at[nurse_index, "Notifications"] = ";".join([notif['message'] for notif in nurse.notifications.notifications])

        # Save back to CSV
        nurses_df.to_csv("nurse.csv", index=False)
        print(f"Nurse {nurse.username}'s information updated successfully.")
    except FileNotFoundError:
        print("nurse.csv file not found.")
    except Exception as e:
        print(f"An error occurred while updating the nurse data: {e}")

def load_patient_data_for_nurse(nursename):
    try:
        patients_df = pd.read_csv("patient.csv")
        nurse_last_name = nursename.split(" ")[-1]  # Assuming the username format is "Nurse Firstname Lastname"

        # Filter patients by nurse's last name
        assigned_patients_df = patients_df[patients_df["Nurse"] == f"Nurse {nurse_last_name}"]

        # Convert to dictionary or list of Patient objects if required
        assigned_patients = assigned_patients_df.to_dict('records')

        # Create a dictionary for storing vitals
        vitals_dict = {}
        for patient in assigned_patients:
            vitals_dict[patient['Name']] = {
                "vitals": {
                    "Heart Rate": None,
                    "Blood Pressure": None,
                    "Temperature": None,
                    "Respiratory Rate": None
                }
            }

        return assigned_patients, vitals_dict

    except FileNotFoundError:
        print("patient.csv file not found.")
    except Exception as e:
        print(f"An error occurred while loading patient data: {e}")

def handle_task_selection(choice, tasks, nurse):
    """Executes the selected task based on user choice."""
    if choice == '14':
        if input("Do you want to logout? (y/n): ").strip().lower() == 'y':
            print("Logging out...")
            return False
    elif choice in tasks:
        tasks[choice]()
    else:
        print("Invalid selection. Please try again.")
    return True

#Dashboard
def nurse_dashboard(nurse):
    """Displays the nurse's dashboard and handles task selection."""
    tasks = {
        '1': nurse.notifications.view_notifications,
        '2': lambda: view_assigned_patients_details(nurse),
        '3': conduct_triage,
        '4': check_shifts,
        '5': lambda: schedule_appointment(nurse),
        '6': lambda: view_scheduled_appointments(nurse),
        '7': lambda: view_patient_records(nurse),
        '8': lambda: update_patient_records(nurse),
        '9': lambda: view_patient_vitals(nurse),
        '10': lambda: log_patient_vitals(nurse),
        '11': lambda: discharge_patient(nurse),
        '12': lambda: request_medical_supplies(nurse),
        '13': nurse.notifications.clear_notifications,
    }

    while True:
        print(f"\n--- Nurse Dashboard for {nurse.username} ---")
        print("""
1.  View Notifications
2.  View Assigned Patients
3.  Conduct Triage
4.  Check Shifts
5.  Schedule Appointment
6.  View Scheduled Appointments
7.  View Patient Records
8.  Update Patient Records
9.  View Patient Vitals
10. Log Patient Vitals
11. Discharge Patient
12. Request Medical Supplies
13. Clear Notifications
14. Logout""")

        choice = input("Select a task (1-14): ").strip()
        if not handle_task_selection(choice, tasks, nurse):
            break
        time.sleep(1)
def view_assigned_patients_details(nurse):
    """Displays detailed information of assigned patients."""
    if not nurse.assigned_patients:
        print("No patients assigned.")
        return

    print("\n--- Patients Assigned to You ---")
    for patient in nurse.assigned_patients:
        print(f"Name: {patient['Name']}, Age: {patient['Age']}, Address: {patient['Address']}, "
              f"Phone: {patient['Phone']}, Username: {patient['Username']}")

def get_patient_name(nurse):
    """Displays a list of patients assigned to the nurse and returns the selected patient's name with error handling."""
    if not nurse.assigned_patients:
        print("No patients assigned.")
        return None

    print("\n--- Patients Assigned to You ---")
    for idx, patient in enumerate(nurse.assigned_patients, start=1):
        print(f"{idx}. {patient['Name']}")

    while True:
        try:
            choice = int(input("Select a patient by number: "))
            if 1 <= choice <= len(nurse.assigned_patients):
                return nurse.assigned_patients[choice - 1]["Name"]
            else:
                print("Invalid number. Please choose a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {e}. Try selecting again.")

def discharge_patient(nurse, patient=None):
    """Handles patient discharge and removes the patient from the nurse's list."""
    if not patient:
        patient = get_patient_name(nurse)
    
    # Check if patient is a valid dictionary with the 'Name' key
    if patient:
        
        # Check if the patient is in the assigned patients list
        for assigned_patient in nurse.assigned_patients:
            print(assigned_patient['Name'])
            print(patient)
            if assigned_patient['Name'] == patient:
                # Notify and remove the patient from the assigned list
                print(f"Patient {patient} has been discharged.")
                nurse.remove_patient(assigned_patient)  # Assuming this method takes the patient dict
                nurse.vitals_dict.pop(patient, None)  # Safely remove from vitals dict
                return
    print(f"Patient {patient} not found in the assigned list.")
    return None

def view_patient_records(nurse):
    """Displays limited records (Reason, Diagnosed diseases, Priority) of a specific patient assigned to the nurse."""
    patient_name = get_patient_name(nurse)
    if not patient_name:
        return  # Exit if no valid patient name is returned
    
    patient_info = next((p for p in nurse.assigned_patients if p["Name"] == patient_name), None)
    if patient_info:
        print(f"\n--- Limited Records for {patient_name} ---")
        for key in ["Reason", "Diagnosed diseases", "Priority"]:
            print(f"{key}: {patient_info[key]}")
    else:
        print("Patient not found or not assigned to you.")

def view_patient_vitals(nurse):
    """Displays the vitals of a specific patient."""
    patient_name = get_patient_name(nurse)
    if not patient_name:
        return
    
    if patient_name in nurse.vitals_dict:
        vitals = nurse.vitals_dict[patient_name]["vitals"]
        print(f"\n--- Vitals for {patient_name} ---")
        for key, value in vitals.items():
            print(f"{key.replace('_', ' ').capitalize()}: {value}")
    else:
        print("Patient not found.")

def request_medical_supplies(nurse):
    """Requests medical supplies."""
    item = input("Enter the item to request: ").strip()
    quantity = input("Enter the quantity: ").strip()
    print(f"Requested {quantity} of {item}.")
    nurse.notifications.add_notification(f"Requested {quantity} of {item}.")

def schedule_appointment(nurse):
    """Assigns a patient to a doctor and schedules an appointment."""
    patients = UserLoader.load_users("patient")  # Load the list of patients
    patient_name = get_patient_name(nurse)
    # Find the patient by name
    selected_patient = next((p for p in patients if p.name == patient_name), None)
    if not selected_patient:
        print(f"Patient '{patient_name}' not found.")
        return

    # Load and list available doctors
    doctors = UserLoader.load_users("doctor")
    print("\nAvailable Doctors:")
    for i, doctor in enumerate(doctors):
        print(f"{i+1}. {doctor.name} - Specialization: {doctor.specialization}")
    
    # Choose doctor by index
    doctor_index = input("Enter the doctor number to assign to the patient: ").strip()
    try:
        doctor_index = int(doctor_index) - 1
        if not (0 <= doctor_index < len(doctors)):
            print("Invalid doctor selection.")
            return
        selected_doctor = doctors[doctor_index]
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    # Schedule appointment
    appointment_date_time = input("Enter appointment date and time (e.g., YYYY-MM-DD HH:MM): ").strip()
    try:
        appointment = Appointment.schedule(
            patient_username=selected_patient.username,
            doctor_username=selected_doctor.username,
            date_time=appointment_date_time,
            patient_list=patients,
            doctor_list=doctors
        )
        print(f"Appointment scheduled successfully for {patient_name} with Dr. {selected_doctor.name} on {appointment_date_time}.")
        nurse.notifications.add_notification(f"Patient {patient_name} assigned to Dr. {selected_doctor.name}.")
    except ValueError as e:
        print(f"Error scheduling appointment: {e}")

def view_scheduled_appointments(nurse):
    """Displays all scheduled appointments for the nurse."""
    appointments = Appointment.all_appointments  # Get all appointments
    if not appointments:
        print("No scheduled appointments found.")
        return
    
    print("\nScheduled Appointments:")
    for appointment in appointments:
        appointment.show_details()

def update_patient_records(nurse):
    """Allows updating of specific fields (Reason, Diagnosed diseases, Priority) in a patient's records."""
    patient_name = get_patient_name(nurse)
    if patient_name is None:
        return  # No patients or selection was invalid

    patient_info = next((p for p in nurse.assigned_patients if p["Name"] == patient_name), None)

    if patient_info:
        print(f"\n--- Update Records for {patient_name} ---")
        print("Available fields to update: Reason, Diagnosed diseases, Priority")
        
        field = input("Enter the field you want to update: ").strip()
        if field not in ["Reason", "Diagnosed diseases", "Priority"]:
            print("Invalid field. Only 'Reason', 'Diagnosed diseases', and 'Priority' can be updated.")
            return

        new_value = input(f"Enter the new value for {field}: ").strip()
        patient_info[field] = new_value  # Update the patient's information
        
        print(f"{field} for {patient_name} updated successfully to: {new_value}")
    else:
        print("Patient not found or not assigned to you.")

def log_patient_vitals(nurse):
    """Logs vitals for a specific patient with validation and graceful degradation."""
    patient_name = get_patient_name(nurse)
    if not patient_name:
        return
    
    vitals = {}
    try:
        vitals["Heart Rate"] = int(input("Enter heart rate: "))
        if not (30 <= vitals["Heart Rate"] <= 200):
            raise ValueError("Heart rate must be between 30 and 200 bpm.")

        vitals["Blood Pressure"] = input("Enter blood pressure (e.g., 120/80): ")
        # Optionally, add format validation for blood pressure

        vitals["Temperature"] = float(input("Enter temperature (°C): "))
        if not (35 <= vitals["Temperature"] <= 42):
            raise ValueError("Temperature should be between 35°C and 42°C.")
        
        vitals["Respiratory Rate"] = int(input("Enter respiratory rate: "))
        if not (10 <= vitals["Respiratory Rate"] <= 30):
            raise ValueError("Respiratory rate should be between 10 and 30 breaths per minute.")
        
        # Log the vitals in the nurse's vitals dictionary
        if patient_name in nurse.vitals_dict:
            nurse.vitals_dict[patient_name]["vitals"] = vitals
            print(f"Vitals logged for {patient_name}.")
        else:
            print("Patient not found.")
    except ValueError as ve:
        print(f"Invalid input: {ve}. Please enter valid data.")
    except Exception as e:
        print(f"An unexpected error occurred while logging vitals: {e}. Please try again.")

# Placeholder functions for to be developed features
def conduct_triage():
    print("Conducting triage...")

def check_shifts():
    print("Checking shifts...")
