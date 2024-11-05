import time
import pandas as pd
import notification
from user import Nurse

# Sample data for patients and their records with multiple symptoms
PATIENT_RECORDS = {
    "Mary Brown": {
        "age": 67,
        "symptoms": ["Shortness of breath", "Fatigue", "Swollen ankles"],
        "vitals": {"heart_rate": 88, "blood_pressure": "140/90", "oxygen_saturation": "92%"},
        "history": ["Diagnosed with congestive heart failure", "Undergoing diuretic therapy", "Hospitalized twice in the last year"]
    },
    "Liam Fox": {
        "age": 54,
        "symptoms": ["Frequent headaches", "Blurred vision"],
        "vitals": {"heart_rate": 76, "blood_pressure": "150/95"},
        "history": ["History of high blood pressure", "Prescribed antihypertensive medication", "Routine eye exams advised"]
    },
    "John Doe": {
        "age": 45,
        "symptoms": ["Dizziness", "High Blood Pressure", "Chest Pain"],
        "vitals": {"heart_rate": 72, "blood_pressure": "130/85"},
        "history": ["Admitted for dizziness", "Prescribed blood pressure medication"]
    },
    "Jane Smith": {
        "age": 32,
        "symptoms": ["Fractured Arm", "Bruising", "Pain"],
        "vitals": {"heart_rate": 78, "blood_pressure": "120/80"},
        "history": ["X-ray taken", "Arm placed in a cast"]
    },
    "Daniel Green": {
        "age": 29,
        "symptoms": ["Abdominal pain", "Nausea", "Vomiting"],
        "vitals": {"heart_rate": 85, "blood_pressure": "118/75"},
        "history": ["Possible food poisoning", "Administered anti-nausea medication"]
    },
    "Emily White": {
        "age": 73,
        "symptoms": ["Joint pain", "Stiffness", "Swelling"],
        "vitals": {"heart_rate": 68, "blood_pressure": "125/80"},
        "history": ["Arthritis diagnosis", "Under physical therapy for joint flexibility"]
    }
}

#CSV Management
def load_nurse_data(nurse_name):
    """Load nurse data from nurse.csv based on the name."""
    try:
        nurses_df = pd.read_csv("nurse.csv")
        nurse_data = nurses_df[nurses_df["Name"] == nurse_name]
        if nurse_data.empty:
            print("No nurse data found for the provided name.")
            return None

        # Extracting the necessary data from the CSV row
        record = nurse_data.iloc[0]
        assigned_patients = record["AssignedPatients"].split(";") if pd.notna(record["AssignedPatients"]) else []
        notifications = record["Notifications"].split(";") if pd.notna(record["Notifications"]) else []

        # Create a Nurse object with loaded data
        nurse = Nurse(
            username=record["Username"],
            assigned_patients=assigned_patients,
            available=record["Availability"],
            can_conduct_triage=record["TriageReady"]
        )

        # Manually add notifications if necessary
        for notification_msg in notifications:
            nurse.notifications.add_notification(notification_msg)

        return nurse

    except FileNotFoundError:
        print("nurse.csv file not found.")
        return None

def update_nurse_data(nurse):
    """Updates the nurse's information in the nurse.csv file."""
    try:
        # Load the CSV into a DataFrame
        nurses_df = pd.read_csv("nurse.csv")
        
        # Check if the nurse exists in the CSV
        nurse_index = nurses_df.index[nurses_df["Username"] == nurse.username].tolist()
        
        if not nurse_index:
            print(f"No record found for nurse {nurse.username}. Cannot update.")
            return
        
        # Get the first index of the matched nurse
        nurse_index = nurse_index[0]

        # Update the necessary fields
        nurses_df.at[nurse_index, "AssignedPatients"] = ";".join(nurse.assigned_patients)
        nurses_df.at[nurse_index, "Availability"] = nurse.available
        nurses_df.at[nurse_index, "TriageReady"] = nurse.can_conduct_triage
        nurses_df.at[nurse_index, "Notifications"] = ";".join(
            [n['message'] for n in nurse.notifications.notifications]
        )

        # Save the updated DataFrame back to CSV
        nurses_df.to_csv("nurse.csv", index=False)
        print(f"Nurse {nurse.username}'s information updated successfully.")

    except FileNotFoundError:
        print("nurse.csv file not found.")
    except Exception as e:
        print(f"An error occurred while updating the nurse data: {e}")

def handle_task_selection(choice, tasks, nurse):
    """Executes the selected task based on user choice."""
    if choice == '15':
        if input("Do you want to logout? (y/n): ").strip().lower() == 'y':
            print("Logging out...")
            return False
    elif choice in tasks:
        tasks[choice]()
    else:
        print("Invalid selection. Please try again.")
    return True

def get_patient_name_input(prompt="Enter the patient's name: "):
    """Prompt for and return a patient name input."""
    return input(prompt).strip()


def nurse_dashboard(nurse):
    """Displays the nurse's dashboard and handles task selection."""
    tasks = {
        '1': nurse.notifications.view_notifications,
        '2': nurse.view_assigned_patients,
        '3': conduct_triage,
        '4': check_shifts,
        '5': schedule_appointment,
        '6': view_scheduled_appointments,
        '7': update_patient_records,
        '8': log_patient_vitals,
        '9': view_patient_records,
        '10': view_patient_vitals,
        '11': lambda: discharge_patient(nurse),
        '12': lambda: request_medical_supplies(nurse),
        '13': view_patient_history,
        '14': nurse.notifications.clear_notifications,
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
7.  Update Patient Records
8.  Log Patient Vitals
9.  View Patient Records
10. View Patient Vitals
11. Discharge Patient
12. Request Medical Supplies
13. View Patient History
14. Clear Notifications
15. Logout""")

        choice = input("Select a task (1-15): ").strip()
        if not handle_task_selection(choice, tasks, nurse):
            break
        time.sleep(1)

def discharge_patient(nurse, patient=None):
    """Handles patient discharge and removes the patient from the nurse's list."""
    if not patient:
        patient = get_patient_name_input("Enter the patient's name to discharge: ")
    
    if patient in nurse.assigned_patients:
        # Notify and remove the patient from the assigned list
        print(f"Patient {patient} has been discharged.")
        nurse.remove_patient(patient)
        return patient  # Return patient for the decorator to capture
    else:
        print(f"Patient {patient} not found in the assigned list.")
        return None

def view_patient_records():
    """Displays detailed records of a specific patient."""
    patient = input("Enter the patient's name: ").strip()
    if patient in PATIENT_RECORDS:
        print(f"\n--- Records for {patient} ---")
        for key, value in PATIENT_RECORDS[patient].items():
            if key != "vitals" and key != "history":
                if key == "symptoms":
                    print(f"Symptoms: {', '.join(value)}")
                else:
                    print(f"{key.capitalize()}: {value}")
    else:
        print("Patient not found.")

def view_patient_vitals():
    """Displays the vitals of a specific patient."""
    patient = get_patient_name_input()
    if patient in PATIENT_RECORDS:
        vitals = PATIENT_RECORDS[patient]["vitals"]
        print(f"\n--- Vitals for {patient} ---")
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

def view_patient_history():
    """Displays the medical history of a specific patient."""
    patient = get_patient_name_input()
    if patient in PATIENT_RECORDS:
        print(f"\n--- Medical History for {patient} ---")
        for event in PATIENT_RECORDS[patient]["history"]:
            print(f"- {event}")
    else:
        print("Patient not found.")

# Placeholder functions for to be developed features
def conduct_triage():
    print("Conducting triage...")

def check_shifts():
    print("Checking shifts...")

def schedule_appointment():
    print("Scheduling an appointment...")

def view_scheduled_appointments():
    print("Viewing scheduled appointments...")

def update_patient_records():
    print("Updating patient records...")

def log_patient_vitals():
    print("Logging patient vitals...")

def run_nurse_portal(nurse_name):
    """Runs the nurse portal after a successful login."""
    # Call login function from login.py
    if nurse_name:
        nurse = load_nurse_data(nurse_name)
        if nurse:
            print(f"Welcome, Nurse {nurse.username}!")
            time.sleep(1)
            nurse_dashboard(nurse)
        else:
            print("Error loading nurse dashboard.")

if __name__ == "__main__":
    run_nurse_portal("Carol Lee")