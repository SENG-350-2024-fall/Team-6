import pandas as pd
from data_stores import all_users

class Appointment:
    all_appointments = []  # Class attribute to store all appointments

    def __init__(self, patient, doctor, date_time):
        self.patient = patient
        self.doctor = doctor
        self.date_time = date_time
        self.status = "Scheduled"  # Automatically set status to "Scheduled"
        Appointment.all_appointments.append(self)  # Add new appointment to shared list

    @staticmethod
    def schedule(patient_username, doctor_username, date_time, patient_list, doctor_list):
        patient = next((p for p in patient_list if p.username == patient_username), None)
        doctor = next((d for d in doctor_list if d.username == doctor_username), None)

        if patient is None:
            raise ValueError(f"Patient with username '{patient_username}' not found.")
        if doctor is None:
            raise ValueError(f"Doctor with username '{doctor_username}' not found.")

        # Create a new appointment and add it to the shared list automatically
        return Appointment(patient, doctor, date_time)

    def cancel(self):
        self.status = "Cancelled"

    def reschedule(self, new_date_time):
        self.date_time = new_date_time
        self.status = "Rescheduled"
        return True

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def show_details(self):
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
    patients, doctors = all_users.get('patient', {}), all_users.get('doctor', {})
    df = pd.read_csv("appointment.csv")

    def find_user_by_username(users, username):
        return next((user for user in users if user.username == username), None)
    
    for _, row in df.iterrows():
        patient = find_user_by_username(patients, row['patient_username'])
        doctor = find_user_by_username(doctors, row['doctor_username'])
        
        if patient and doctor:
            Appointment(patient, doctor, row['date_time'])
        else:
            print(f"Patient or Doctor not found for usernames: {row['patient_username']}, {row['doctor_username']}")

# This populates the Appointment.all_appointments list
load_appointments()
