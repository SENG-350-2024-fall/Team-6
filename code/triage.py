import pandas as pd
from csv import writer
from datetime import date
import warnings

warnings.filterwarnings("ignore")

# Base class for notifying
class Notifier:
    def notify(self):
        raise NotImplementedError("Notify method not implemented.")

    def additional_notification(self):
        raise NotImplementedError("Notify method not implemented.")


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
        self.nurses = []
        self.triage_outcome = "Pending Nurse's Report"
        self.priority = "Low"
        self.triage_type = "Zoom"
        self.date = date.today()
        self.patient_info = {"Name": "John Doe", "Mode": self.triage_type, "Priority": self.priority}
        self.nurse_info = {"Name": "Nurse Smith", "Mode": self.triage_type}
        return

    def set_patient_info(self, patient_info):
        self.patient_info = patient_info

    def set_nurse_info(self, nurse_info):
        self.nurse_info = nurse_info

    def get_patient_info(self):
        return self.patient_info

    def get_nurse_info(self):
        return self.nurse_info
        
    def get_priority(self):
        return self.priority
        
    def get_mode(self):
        return self.triage_type
        
    def perform_triage(self):
        mode = input("Input Mode Number: 1. Zoom   2. Phone Call:  ")
        self.triage_type = "Zoom" if mode == "1" else "Phone Call"

        self.priority = input("Priority: 1. Low   2. Meduim   3. High  ")

        if self.priority == "3":
            print("Please Call 911 or Go to Hospital!!")
            exit(0)

        self.priorities = ["Low", "Meduim", "High"]
        self.priority = self.priorities[int(self.priority)]
        
    def notify_patient_nurse(self):
        # Create notifiers
        patient_notifier = PatientNotifier(self.get_patient_info())
        nurse_notifier = NurseNotifier(self.get_nurse_info())

        # Use the decorator for simultaneous notifications
        simultaneous_notifier = SimultaneousNotifier(patient_notifier, nurse_notifier)
        simultaneous_notifier.notify()


# Entry point
if __name__ == "__main__":
    triage_instance = Triage()
    triage_instance.perform_triage()