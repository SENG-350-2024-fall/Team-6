import os
import time

# Sample patient data
patients = [
    {"id": 1, "name": "John Doe", "age": 30, "medical_record": "MRN001"},
    {"id": 2, "name": "Jane Smith", "age": 25, "medical_record": "MRN002"},
    {"id": 3, "name": "Alice Johnson", "age": 40, "medical_record": "MRN003"}
]

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def view_patient_list():
    print("Patient List:")
    for patient in patients:
        print(f"ID: {patient['id']}, Name: {patient['name']}, Age: {patient['age']}, Medical Record: {patient['medical_record']}")
    time.sleep(2)  # Simulating a delay for viewing the list

def search_patient():
    patient_id = input("Enter the Patient ID to search: ")
    for patient in patients:
        if str(patient['id']) == patient_id:
            print(f"Found Patient: ID: {patient['id']}, Name: {patient['name']}, Age: {patient['age']}, Medical Record: {patient['medical_record']}")
            time.sleep(2)  # Simulating a delay for viewing patient details
            return
    print("Patient not found.")
    time.sleep(2)

def serve_patient():
    print("Serving Patient...")
    # Here you would implement the logic to serve a patient
    time.sleep(2)

def update_patient_record():
    patient_id = input("Enter the Patient ID to update: ")
    for patient in patients:
        if str(patient['id']) == patient_id:
            # Here you would implement the logic to update the patient's record
            print(f"Updating record for {patient['name']}...")
            time.sleep(2)  # Simulating a delay for updating
            return
    print("Patient not found.")
    time.sleep(2)

def log_out():
    print("Logging out...")
    time.sleep(1)
    return False  # Return False to indicate the user is logging out

def doctor_dashboard():
    logged_in = True
    while logged_in:
        clear_terminal()
        print(" =============================")
        print("|| Welcome to the Doctor's Dashboard ||")
        print(" =============================\n")
        print("Please select an option:\n")
        print("1. View Patient List")
        print("2. Search Patient")
        print("3. Serve Patient")
        print("4. Update Patient Record")
        print("5. Log Out\n")

        choice = input("Enter the number corresponding to your choice:\n")

        if choice == '1':
            view_patient_list()
        elif choice == '2':
            search_patient()
        elif choice == '3':
            serve_patient()
        elif choice == '4':
            update_patient_record()
        elif choice == '5':
            logged_in = log_out()
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(2)

if __name__ == "__main__":
    doctor_dashboard()
