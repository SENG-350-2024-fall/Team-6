import os
import time
import re
from data_stores import all_users
from appointment import Appointment
from notification import Notification

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def view_patient_list(patients):
    print("Patient List:")
    for i, patient in enumerate(patients, start=1):
        print(f"{i}. Name: {patient.name}, Age: {patient.age}, Address: {patient.address}, Phone: {patient.phone_number}")
    
    input("\nPress Enter to go back to the menu...")

def search_patient(patients):
    patient_name = input("Enter the Patient Name to search: ").strip()
    pattern = re.compile(patient_name, re.IGNORECASE)

    for patient in patients:
        if pattern.search(patient.name):
            print(f"Found Patient: Name: {patient.name}, Age: {patient.age}, Address: {patient.address}, Phone: {patient.phone_number}")
            time.sleep(2)
            return
    print("Patient not found.")
    time.sleep(1)

def view_profile(doctor):
    """Display the profile of a doctor with the given username."""
    if doctor:
        print("Your Profile:")
        print(f"Name: {doctor.name}")
        print(f"Age: {doctor.age}")
        print(f"Address: {doctor.address}")
        print(f"Phone Number: {doctor.phone_number}")
        print(f"Username: {doctor.username}")
        print(f"Specialization: {doctor.specialization}")
        print(f"Available: {'Yes' if doctor.available else 'No'}")
    else:
        print("Profile not found. Contact the System Administrator.")
    input("\nPress Enter to go back to the menu...")

def view_appointments(doctor_appointments):
    if doctor_appointments:
        print("Your Appointments:")
        for appt in doctor_appointments:
            appt.show_details()  # Call the method to show details of each appointment
            print()  # Add space between appointments
    else:
        print("You have no appointments scheduled.")
    
    input("\nPress Enter to go back to the menu...")

def serve_patient(doctor_appointments):
    """
    Displays all appointments and allows the doctor to select a patient to serve.
    Once served, the appointment is removed from the list.
    """
    if not doctor_appointments:
        print("No appointments to serve.")
        time.sleep(2)
        return
    
    print("Appointments List:")
    for idx, appt in enumerate(doctor_appointments, start=1):
        print(f"{idx}. Patient: {appt.patient.name} | Date & Time: {appt.date_time}")
    
    try:
        choice = int(input("\nEnter the number of the appointment you want to serve: ")) - 1
        
        if 0 <= choice < len(doctor_appointments):
            selected_appointment = doctor_appointments[choice]
            selected_appointment.patient.status = "Served"
            print(f"Serving patient {selected_appointment.patient.name}...")
            time.sleep(2)
            doctor_appointments.pop(choice)  # Remove the served appointment
            print("Appointment served and removed from the list.")
        else:
            print("Invalid selection. Please try again.")
            time.sleep(1)
    except ValueError:
        print("Invalid input. Please enter a valid appointment number.")
        time.sleep(1)

    
def update_patient_record(patients, doctor):
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
            doctor.notifications.add_notification(f"Updated record for patient {patient.name}")
            time.sleep(1)
            return
    print("Patient not found.")
    time.sleep(2)

def view_notifications(doctor):
    """View notifications for the doctor."""
    doctor.notifications.view_notifications()
    time.sleep(2)

def log_out():
    print("Logging out...")
    time.sleep(1)
    return False

def doctor_dashboard(user):
    # Retrieve all patient instances from all_users
    patients = all_users.get('patient', [])
    doctor_appointments = Appointment.all_appointments
    doctor_appointments = [appt for appt in doctor_appointments if appt.doctor.username == user.username]

    logged_in = True
    while logged_in:
        clear_terminal()
        print(f"Welcome Dr.{user.name} !!\n")
        time.sleep(1)
        clear_terminal()
        print(" =============================")
        print(f"|| Dr.{user.name} Dashboard ||")
        print(" =============================\n")
        print("Please select an option:\n")
        print("1. View Patient List")
        print("2. Search Patient")
        print("3. Serve Patient")
        print("4. Update Patient Record")
        print("5. View Notifications")
        print("6. View Profile")
        print("7. View Appointments")
        print("8. Log Out\n")

        choice = input("Enter the number corresponding to your choice:\n")

        if choice == '1':
            view_patient_list(patients)
        elif choice == '2':
            search_patient(patients)
        elif choice == '3':
            serve_patient(doctor_appointments)
        elif choice == '4':
            update_patient_record(patients, user)
        elif choice == '5':
            view_notifications(user)
        elif choice == '6':
            view_profile(user)
        elif choice == '7':
            view_appointments(doctor_appointments)
        elif choice == '8':
            logged_in = log_out()
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    # Replace 'User' in the print statement with the actual username of the doctor
    doctor_dashboard("Doctor")  # Replace with actual username if needed

