import os
import time
from user import Patient
from data_stores import all_users

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def view_ed_capacity():
    patients = all_users.get('patient', [])
    ed_capacity = 10  # Assuming fixed capacity; this could be dynamic
    print(f"Current ED Capacity: {len(patients)}/{ed_capacity} patients.")
    time.sleep(2)

def assign_patient_to_nurse():
    patients = all_users.get('patient', [])
    nurses = all_users.get('nurse', [])  # Retrieve the list of nurses
    patient_username = input("Enter the Patient Username to assign to a nurse: ")
    
    # Find the patient by username
    patient = next((p for p in patients if p.username.lower() == patient_username.lower()), None)
    
    if patient:
        print("Available Nurses:")
        for i, nurse in enumerate(nurses, 1):
            print(f"{i}. {nurse.name}")  # Access the nurse's name
        nurse_choice = int(input("Enter the number corresponding to the nurse:\n"))
        
        if 1 <= nurse_choice <= len(nurses):
            patient.assigned_nurse = nurses[nurse_choice - 1].name  # Assign nurse by name
            print(f"Assigned {nurses[nurse_choice - 1].name} to {patient.username}.")
            time.sleep(2)
            return
        else:
            print("Invalid nurse selection.")
            time.sleep(2)
            return
    print("Patient not found.")
    time.sleep(2)

def log_incoming_patient():
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
    print(f"Logged new patient: {name} (Username: {new_patient.username}).")
    time.sleep(2)

def log_out():
    print("Logging out...")
    time.sleep(1)
    return False

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
        print("4. Log Out\n")

        choice = input("Enter the number corresponding to your choice:\n")

        if choice == '1':
            view_ed_capacity()
        elif choice == '2':
            assign_patient_to_nurse()
        elif choice == '3':
            log_incoming_patient()
        elif choice == '4':
            logged_in = log_out()
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(2)

if __name__ == "__main__":
    ed_staff_dashboard()
