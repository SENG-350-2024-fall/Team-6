import pandas as pd
import time
from data_stores import all_users

class Appointment:
    def __init__(self, patient, doctor, date_time):
        self.patient = patient
        self.doctor = doctor
        self.date_time = date_time
        self.status = "Scheduled"  # Automatically set status to "Scheduled"

    @staticmethod
    def schedule(patient_username, doctor_username, date_time, patient_list, doctor_list):
        # Find the patient by username
        patient = next((p for p in patient_list if p.username == patient_username), None)
        # Find the doctor by username
        doctor = next((d for d in doctor_list if d.username == doctor_username), None)

        if patient is None:
            raise ValueError(f"Patient with username '{patient_username}' not found.")
        if doctor is None:
            raise ValueError(f"Doctor with username '{doctor_username}' not found.")

        # Create and return a new appointment
        return Appointment(patient, doctor, date_time)

    def cancel(self):
        # Logic to cancel the appointment
        self.status = "Cancelled"

    def reschedule(self, new_date_time):
        # Logic to reschedule the appointment
        self.date_time = new_date_time
        self.status = "Rescheduled"
        return True

    def get_status(self):
        # Returns the current status of the appointment
        return self.status

    def set_status(self, status):
        # Updates the status of the appointment
        self.status = status

    def show_details(self):
        # Displays detailed information about the appointment
        print("\n" + "=" * 40)
        print("         Appointment Details        ")
        print("=" * 40)
        print(f"Date & Time   : {self.date_time}")
        print(f"Status        : {self.status}")
        print("\nPatient Information:")
        print(f"  Name        : {self.patient.name}")
        print(f"  Age         : {self.patient.age}")
        print(f"  Address     : {self.patient.address}")
        print(f"  Phone       : {self.patient.phone_number}")
        print("\nDoctor Information:")
        print(f"  Name        : {self.doctor.name}")
        print(f"  Specialization: {self.doctor.specialization}")
        print(f"  Available   : {'Yes' if self.doctor.available else 'No'}")
        print("=" * 40 + "\n")


def load_appointments():
    # Load patients and doctors from a predefined function or database
    patients, doctors = all_users.get('patient', {}), all_users.get('doctor', {})
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv("appointment.csv")

    appointments = []

    # Helper function to find a user by username in a list
    def find_user_by_username(users, username):
        for user in users:
            if user.username == username:
                return user
        return None
    
    # Iterate over each row of the DataFrame
    for _, row in df.iterrows():
        patient_username = row['patient_username']
        doctor_username = row['doctor_username']
        date_time = row['date_time']  # Make sure this matches your CSV header
        
        # Retrieve the patient and doctor objects from the lists
        patient = find_user_by_username(patients, patient_username)
        doctor = find_user_by_username(doctors, doctor_username)

        # Only create an Appointment if both patient and doctor are found
        if patient is not None and doctor is not None:
            appointment = Appointment(patient, doctor, date_time)
            appointments.append(appointment)
        else:
            print(f"Patient or Doctor not found for usernames: {patient_username}, {doctor_username}")
    
    return appointments