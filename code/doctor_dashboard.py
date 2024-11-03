import os
import time
from data_stores import all_users
from notification import Notification
doctor_notifications = Notification()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def view_patient_list(patients):
    print("Patient List:")
    for i, patient in enumerate(patients, start=1):
        print(f"{i}. Name: {patient.name}, Age: {patient.age}, Address: {patient.address}, Phone: {patient.phone_number}")
    time.sleep(2)

def search_patient(patients):
    patient_name = input("Enter the Patient Name to search: ").strip()
    for patient in patients:
        if patient.name.lower() == patient_name.lower():
            print(f"Found Patient: Name: {patient.name}, Age: {patient.age}, Address: {patient.address}, Phone: {patient.phone_number}")
            time.sleep(2)
            return
    print("Patient not found.")
    time.sleep(2)

def serve_patient():
    print("Serving Patient...")
    time.sleep(2)
    
def update_patient_record(patients):
    patient_name = input("Enter the Patient Name to update: ").strip()
    for patient in patients:
        if patient.name.lower() == patient_name.lower():
            print(f"Updating record for {patient.name}...")
            # Example of updating patient details
            new_phone = input("Enter new phone number (leave blank to keep current): ")
            if new_phone:
                patient.phone_number = new_phone
                print("Patient phone number updated.")
            # Add a notification for the updated patient record
            doctor_notifications.add_notification(f"Updated record for patient {patient.name}")
            time.sleep(2)
            return
    print("Patient not found.")
    time.sleep(2)

def view_notifications():
    """View notifications for the doctor."""
    doctor_notifications.view_notifications()
    time.sleep(2)

def log_out():
    print("Logging out...")
    time.sleep(1)
    return False

def doctor_dashboard(user):
    # Retrieve all patient instances from all_users
    patients = all_users.get('patient', [])
    
    if not patients:
        print("No patients found in the system. Exiting.")
        return

    logged_in = True
    while logged_in:
        clear_terminal()
        print(f"Welcome Dr.{user} !!\n")
        time.sleep(2)
        print(" =============================")
        print("|| Welcome to the Doctor's Dashboard ||")
        print(" =============================\n")
        print("Please select an option:\n")
        print("1. View Patient List")
        print("2. Search Patient")
        print("3. Serve Patient")
        print("4. Update Patient Record")
        print("5. View Notifications")
        print("6. Log Out\n")

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
            view_notifications()
        elif choice == '6':
            logged_in = log_out()
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(2)

if __name__ == "__main__":
    # Replace 'User' in the print statement with the actual username of the doctor
    doctor_dashboard("Doctor")  # Replace with actual username if needed
