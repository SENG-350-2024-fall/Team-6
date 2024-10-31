import os
import time
import pandas as pd

# Load patient data from CSV file using pandas
def load_patients_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        # Keep only the relevant columns and rename them
        df = df[['Name', 'Age', 'Address', 'Phone']]  # Selecting only the required columns
        df.columns = ['name', 'age', 'address', 'phone']
        patients = df.to_dict(orient='records')
        return patients
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def view_patient_list(patients):
    print("Patient List:")
    for i, patient in enumerate(patients, start=1):
        print(f"{i}. Name: {patient['name']}, Age: {patient['age']}, Address: {patient['address']}, Phone: {patient['phone']}")
    time.sleep(2)

def search_patient(patients):
    patient_name = input("Enter the Patient Name to search: ")  # Search by name instead
    for patient in patients:
        if patient['name'].lower() == patient_name.lower():  # Case-insensitive search
            print(f"Found Patient: Name: {patient['name']}, Age: {patient['age']}, Address: {patient['address']}, Phone: {patient['phone']}")
            time.sleep(2)
            return
    print("Patient not found.")
    time.sleep(2)

def serve_patient():
    print("Serving Patient...")
    time.sleep(2)

def update_patient_record(patients):
    patient_name = input("Enter the Patient Name to update: ")  # Update by name instead
    for patient in patients:
        if patient['name'].lower() == patient_name.lower():
            print(f"Updating record for {patient['name']}...")
            time.sleep(2)
            return
    print("Patient not found.")
    time.sleep(2)

def log_out():
    print("Logging out...")
    time.sleep(1)
    return False

def doctor_dashboard(user):
    # Load patient data from CSV
    file_path = 'patient.csv'  # Updated to match your new CSV filename
    patients = load_patients_from_csv(file_path)
    
    if not patients:
        print("No patients found in the file. Exiting.")
        return

    logged_in = True
    while logged_in:
        clear_terminal()
        print("Welcome " + user + " !!\n")
        time.sleep(2)
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
            view_patient_list(patients)
        elif choice == '2':
            search_patient(patients)
        elif choice == '3':
            serve_patient()
        elif choice == '4':
            update_patient_record(patients)
        elif choice == '5':
            logged_in = log_out()
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(2)

if __name__ == "__main__":
    doctor_dashboard()
