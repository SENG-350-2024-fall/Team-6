import os
import notification
import hospital
import time
from user import Patient
from data_stores import all_users, UserLoader

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class EdDashboard:
    def __init__(self):
        self.hospital = hospital.Hospital()

    def view_ed_capacity(self):
        current_load = self.hospital.getCurrentEDCapacity()
        total_capacity = self.hospital.edCapacity
        print(f"Current ED Capacity: {current_load}/{total_capacity} patients")
        print(f"Hospital: {self.hospital.getName()}")
        time.sleep(2)


    def log_incoming_patient(self):
        patients = all_users.get('patient', [])
        ed_capacity = 10  # Assuming fixed capacity
        if len(patients) >= ed_capacity:
            print("ED is at full capacity! Cannot log new patient.")
            time.sleep(2)
            return

        name = input("Enter the patient's name: ")
        age = input("Enter the patient's age: ")
        address = input("Enter the patient's address: ")
        phone_number = input("Enter the patient's phone number: ")
        username = input("Enter the patient's username: ")  # Add username input
        password = input("Enter the patient's password: ")  # Add password input

        # Create new patient object
        new_patient = Patient(
            name=name,
            age=int(age),
            address=address,
            phone_number=phone_number,
            username=username,
            password=password
        )

        # Append new patient to the all_users structure
        patients.append(new_patient)
        all_users['patient'] = patients  # Update all_users with the new patient
        self.hospital.incrementED()
        print(f"Logged new patient: {name} (Username: {new_patient.username}).")
        time.sleep(2)

def log_out():
    print("Logging out...")
    time.sleep(1)
    return False

def assign_patient_to_nurse():
    patients = all_users.get('patient', [])
    nurses = all_users.get('nurse', [])  # Retrieve the list of nurses
    patient_username = input("Enter the Patient Username to assign to a nurse: ")

    # Find the patient by username
    patient = next((p for p in patients if p.username.lower() == patient_username.lower()), None)

    if patient:
        nurses = UserLoader.load_users("nurse")
        available_nurses = [nurse for nurse in nurses if nurse.available and nurse.triage_ready]
        if not available_nurses:
            print("No nurses are available for triage.")
            return None

        # Find the nurse with the least assigned patients
        selected_nurse = min(available_nurses, key=lambda nurse: len(nurse.assigned_patients))

        # Update the nurse's assigned patients
        selected_nurse.add_patient(patient.name)
        selected_nurse.notifications.add_notification_for_observer("New Triage to conduct", selected_nurse.username)
    time.sleep(2)

def list_all_patients():
    patients = all_users.get('patient', [])
    if not patients:
        print("No patients currently in the system.")
        time.sleep(2)
        return

    print("\nCurrent Patients:")
    print("-" * 50)
    print(f"{'Name':<20} {'Age':<6} {'Assigned Nurse':<20}")
    print("-" * 50)

    for patient in patients:
        nurse = getattr(patient, 'assigned_nurse', 'Not Assigned')
        print(f"{patient.name:<20} {patient.age:<6} {nurse:<20}")

    print("-" * 50)
    input("\nPress Enter to continue...")

def ed_staff_dashboard(user):
    logged_in = True
    while logged_in:
        clear_terminal()
        print(f"Welcome {user} !!\n")
        print(" =============================")
        print("|| Welcome to the ED Staff Dashboard ||")
        print(" =============================\n")
        print("Please select an option:\n")
        print("1. View ED Capacity")
        print("2. Assign Patient to Nurse")
        print("3. Log Incoming Patient")
        print("4. List All Patients")  # New option
        print("5. Log Out\n")          # Moved to option 5

        choice = input("Enter the number corresponding to your choice:\n")
        dash = EdDashboard()

        if choice == '1':
            dash.view_ed_capacity()
        elif choice == '2':
            assign_patient_to_nurse()
        elif choice == '3':
            dash.log_incoming_patient()
        elif choice == '4':
            list_all_patients()
        elif choice == '5':
            logged_in = log_out()
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(2)
