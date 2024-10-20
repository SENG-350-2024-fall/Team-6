import os
import time

patients = [
    {"id": 1, "name": "John Doe", "age": 30, "medical_record": "MRN001", "assigned_nurse": None},
    {"id": 2, "name": "Jane Smith", "age": 25, "medical_record": "MRN002", "assigned_nurse": None},
    {"id": 3, "name": "Alice Johnson", "age": 40, "medical_record": "MRN003", "assigned_nurse": None}
]

nurses = ["Nurse Alice", "Nurse Bob", "Nurse Charlie"]
ed_capacity = 10

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def view_ed_capacity():
    print(f"Current ED Capacity: {len(patients)}/{ed_capacity} patients.")
    time.sleep(2)

def assign_patient_to_nurse():
    patient_id = input("Enter the Patient ID to assign to a nurse: ")
    for patient in patients:
        if str(patient['id']) == patient_id:
            print("Available Nurses:")
            for i, nurse in enumerate(nurses, 1):
                print(f"{i}. {nurse}")
            nurse_choice = int(input("Enter the number corresponding to the nurse:\n"))
            if 1 <= nurse_choice <= len(nurses):
                patient['assigned_nurse'] = nurses[nurse_choice - 1]
                print(f"Assigned {nurses[nurse_choice - 1]} to {patient['name']}.")
                time.sleep(2)
                return
            else:
                print("Invalid nurse selection.")
                time.sleep(2)
                return
    print("Patient not found.")
    time.sleep(2)

def log_incoming_patient():
    name = input("Enter the patient's name: ")
    age = input("Enter the patient's age: ")
    medical_record = input("Enter the patient's medical record number: ")

    new_patient = {
        "id": len(patients) + 1,
        "name": name,
        "age": int(age),
        "medical_record": medical_record,
        "assigned_nurse": None
    }

    if len(patients) < ed_capacity:
        patients.append(new_patient)
        print(f"Logged new patient: {name} (ID: {new_patient['id']}).")
    else:
        print("ED is at full capacity! Cannot log new patient.")
    time.sleep(2)

def log_out():
    print("Logging out...")
    time.sleep(1)
    return False

def ed_staff_dashboard():
    logged_in = True
    while logged_in:
        clear_terminal()
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
