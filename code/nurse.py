import time

# Constants
NURSE_CREDENTIALS = {
    "alice": "password123",
    "bob": "securepass",
}

new_notification = 0
notifications = []

# Sample data for patients and their records with multiple symptoms
PATIENT_RECORDS = {
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
    }
}


class Nurse:
    """Represents a Nurse."""
    def __init__(self, username):
        self.username = username
        self.assigned_patients = []
        self.available = True
        self.can_conduct_triage = True
        self.shifts = []

    def add_patient(self, patient):
        self.assigned_patients.append(patient)
        add_notification(f"Patient {patient} has been assigned to you.")

    def remove_patient(self, patient):
        """Removes a discharged patient from the assigned list."""
        if patient in self.assigned_patients:
            self.assigned_patients.remove(patient)
            add_notification(f"Patient {patient} has been removed from your care.")
        else:
            print(f"Patient {patient} is not in your assigned list.")

    def __str__(self):
        return f"Nurse: {self.username}"


def authenticate_nurse():
    """Authenticates nurse login using username and password."""
    print("\n--- Nurse Login ---")
    while True:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        if NURSE_CREDENTIALS.get(username) == password:
            print(f"Welcome, {username}!")
            return Nurse(username)
        else:
            print("Invalid credentials. Please try again.")


def view_notifications():
    """Displays notifications and offers option to clear them."""
    global new_notification
    if notifications:
        print(f"\nYou have {new_notification} new notification(s)")
        print("\n--- Notifications ---")
        for i, notification in enumerate(notifications, 1):
            print(f"{i}. {notification}")
    else:
        print("\nYou have no new notifications.")

    if input("Clear notifications? (y/n): ").strip().lower() == 'y':
        clear_notifications()


def add_notification(message):
    """Adds a new notification."""
    global new_notification
    notifications.append(message)
    new_notification += 1


def clear_notifications():
    """Clears all notifications."""
    global new_notification
    notifications.clear()
    new_notification = 0
    print("All notifications cleared!")


def nurse_dashboard(nurse):
    """Displays the nurse's dashboard and handles task selection."""
    tasks = {
        '1': view_notifications,
        '2': lambda: view_assigned_patients(nurse),
        '3': conduct_triage,
        '4': check_shifts,
        '5': schedule_appointment,
        '6': view_scheduled_appointments,
        '7': update_patient_records,
        '8': log_patient_vitals,
        '9': view_patient_records,
        '10': view_patient_vitals,
        '11': lambda: discharge_patient(nurse),
        '12': request_medical_supplies,
        '13': view_patient_history,
    }

    while True:
        print(f"\n--- Nurse Dashboard for {nurse.username} ---")
        print("""\
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
14. Logout""")

        choice = input("Select a task (1-14): ").strip()
        if choice == '14':
            if input("Do you want to logout? (y/n): ").strip().lower() == 'y':
                print("Logging out...")
                break
        elif choice in tasks:
            tasks[choice]()
        else:
            print("Invalid selection. Please try again.")
        time.sleep(1)


def view_assigned_patients(nurse):
    """Displays the patients assigned to the nurse."""
    if nurse.assigned_patients:
        print("Assigned Patients:")
        for patient in nurse.assigned_patients:
            print(f"- {patient}")
    else:
        print("No patients assigned.")


def discharge_patient(nurse):
    """Handles patient discharge and removes the patient from the nurse's list."""
    patient = input("Enter the patient's name to discharge: ").strip()
    if patient in PATIENT_RECORDS:
        print(f"Patient {patient} has been discharged.")
        nurse.remove_patient(patient)  # Remove from nurse's assigned list
        add_notification(f"Patient {patient} has been discharged.")
    else:
        print("Patient not found.")


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
    patient = input("Enter the patient's name: ").strip()
    if patient in PATIENT_RECORDS:
        vitals = PATIENT_RECORDS[patient]["vitals"]
        print(f"\n--- Vitals for {patient} ---")
        for key, value in vitals.items():
            print(f"{key.replace('_', ' ').capitalize()}: {value}")
    else:
        print("Patient not found.")


def request_medical_supplies():
    """Requests medical supplies."""
    item = input("Enter the item to request: ").strip()
    quantity = input("Enter the quantity: ").strip()
    print(f"Requested {quantity} of {item}.")
    add_notification(f"Requested {quantity} of {item}.")


def view_patient_history():
    """Displays the medical history of a specific patient."""
    patient = input("Enter the patient's name: ").strip()
    if patient in PATIENT_RECORDS:
        print(f"\n--- Medical History for {patient} ---")
        for event in PATIENT_RECORDS[patient]["history"]:
            print(f"- {event}")
    else:
        print("Patient not found.")


# Placeholder functions for existing features
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


def run_nurse_portal():
    """Starts the nurse portal after successful login."""
    nurse = authenticate_nurse()
    nurse.add_patient("John Doe")
    time.sleep(1)
    view_notifications()
    time.sleep(0.5)
    nurse_dashboard(nurse)


if __name__ == "__main__":
    run_nurse_portal()