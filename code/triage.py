import pandas as pd
from csv import writer
from datetime import date
import warnings
from user import UserLoader

warnings.filterwarnings("ignore")

# Base class for notifying
class Notifier:
    def notify(self):
        print("Both Patient and Nurse are Notified.")
        return

    def additional_notification(self):
        print("Both Patient and Nurse are Notified.")


# Concrete Notifier for Patient
class PatientNotifier(Notifier):
    def __init__(self, patient_info):
        self.patient_info = patient_info

    def notify(self):
        # Simulate notifying the patient
        print(
            f"Notifying patient: {self.patient_info['Name']} with {self.patient_info['Priority']} Priority via {self.patient_info['Mode']}."
        )


# Concrete Notifier for Nurse
class NurseNotifier(Notifier):
    def __init__(self, nurse_info):
        self.nurse_info = nurse_info

    def notify(self):
        # Simulate notifying the nurse
        print(
            f"Notifying nurse: {self.nurse_info['Name']} via {self.nurse_info['Mode']}."
        )


# Decorator for notification
class NotificationDecorator(Notifier):
    def __init__(self, notifier):
        self.notifier = notifier

    def notify(self):
        self.notifier.notify()
        self.additional_notification()

    def additional_notification(self):
        raise NotImplementedError("Additional notification method not implemented.")


# Concrete decorator for simultaneous notifications
class SimultaneousNotifier(NotificationDecorator):
    def __init__(self, patient_notifier, nurse_notifier):
        super().__init__(patient_notifier)
        self.nurse_notifier = nurse_notifier

    def additional_notification(self):
        self.nurse_notifier.notify()


# Triage class
class Triage:

    def __init__(self):
        self.patients = []
        self.triage_outcome = "Pending Nurse's Report"
        self.priority = "Low"
        self.triage_type = "Zoom"
        self.date = date.today()
        self.patient_info = {"Name": "John Doe", "Mode": self.triage_type, "Priority": self.priority}
        self.nurse_info = self.assign_available_nurse()

    def assign_available_nurse(self):
        """Assigns the triage to the nurse who is available and has the fewest assigned patients."""
        nurses = UserLoader.load_users("nurse")
        available_nurses = [nurse for nurse in nurses if nurse.available and nurse.triage_ready]
        if not available_nurses:
            print("No nurses are available for triage.")
            return None

        # Find the nurse with the least assigned patients
        selected_nurse = min(available_nurses, key=lambda nurse: len(nurse.assigned_patients))
        nurse_info = {"Name": selected_nurse.name, "Mode": self.triage_type}
        
        # Update the nurse's assigned patients
        selected_nurse.add_patient(self.patient_info["Name"])
        selected_nurse.notifications.add_notification_for_observer("New Triage to conduct", selected_nurse.username)
        return nurse_info

    def set_patient_info(self, patient_info):
        self.patient_info = patient_info

    def set_nurse_info(self, nurse_info):
        self.nurse_info = nurse_info
    
    #This returns a dictionary
    def get_patient_info(self):
        return self.patient_info
    
    #This returns a dictionary
    def get_nurse_info(self):
        return self.nurse_info
        
    def get_priority(self):
        return self.priority
        
    def get_mode(self):
        return self.triage_type
        
    def perform_triage(self):
        mode = input("Input Mode Number: 1 = Zoom, 2 = Phone Call  ")
        self.triage_type = "Zoom" if mode == "1" else "Phone Call"

        self.priority = input("Priority: 1 = Low, 2 = Meduim, 3 = High  ")

        if self.priority == "3":
            print("Please Call 911 or Go to Hospital!!")
            exit(0)

        self.priorities = ["Low", "Meduim", "High"]
        self.priority = self.priorities[int(self.priority) - 1]
        
    def notify_patient_nurse(self):
        # Create notifiers
        patient_notifier = PatientNotifier(self.get_patient_info())
        nurse_notifier = NurseNotifier(self.get_nurse_info())

        # Use the decorator for simultaneous notifications
        simultaneous_notifier = SimultaneousNotifier(patient_notifier, nurse_notifier)
        simultaneous_notifier.notify()

'''
# Entry point
if __name__ == "__main__":
    triage_instance = Triage()
    triage_instance.perform_triage()
'''