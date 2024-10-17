import time

# Initialize notification variables
new_notification = 0
notifications = []

class Nurse:
    def __init__(self, username):
        self.username = username
        self.assigned_patients = []  # List of patients under the nurse's care
        self.available = True  # Availability status
        self.can_conduct_triage = True  # Triage capability
        self.shifts = []

    def add_patient(self, patient):
        self.assigned_patients.append(patient)
        add_notification(f"Patient {patient} has been assigned to you.")

def view_notifications():
    global new_notification
    if new_notification > 0:
        print("You have " + str(new_notification) + " new notifications")
        print("\n--- Notifications ---")
        for i, notification in enumerate(notifications, 1):
            print(f"{i}. {notification}")
    else:
        print("\nYou have No new notifications.")
    
    notificationclear = input("Clear notifications? y/n: ")
    if notificationclear.lower() == 'y':
        clear_notifications()

def add_notification(message):
    global new_notification
    notifications.append(message)
    new_notification += 1

def clear_notifications():
    notifications.clear()
    global new_notification
    new_notification = 0
    print("All notifications cleared!")

def nurse_dashboard(nurse):
    """Function to display the nurse's dashboard."""
    print("\n--- Nurse Dashboard ---")
    print("1. View Notifications")
    print("2. View Assigned Patients")
    print("3. Conduct Triage")
    print("4. Check Shifts")
    print("5. Schedule Appointment")
    print("6. View Scheduled Appointments")
    print("7. Update Patient Records")
    print("8. Log Patient Vitals")
    print("9. Staff Chat")
    print("10. Logout")
    
    task = input("Select a task by entering the corresponding number: ")

    if task == '1':
        view_notifications()
    elif task == '2':
        view_assigned_patients(nurse)
    elif task == '3':
        conduct_triage()
    elif task == '4':
        check_shifts()
    elif task == '5':
        schedule_appointment()
    elif task == '6':
        view_scheduled_appointments()
    elif task == '7':
        update_patient_records()
    elif task == '8':
        log_patient_vitals()
    elif task == '9':
        staff_chat()
    elif task == '10':
        logout = input("Do you want to logout? y/n: ")
        if (logout == 'y'):
            print("Logging out...")
            return  # Exit the dashboard
    else:
        print("Invalid selection, please try again.")
    
    time.sleep(1)
    nurse_dashboard(nurse)  # Call the dashboard again after completing a task

def view_assigned_patients(nurse):
    print("Assigned Patients:")
    if not nurse.assigned_patients:
        print("No patients assigned.")
    else:
        for patient in nurse.assigned_patients:
            print(f"- {patient}")  # Display each assigned patient

def conduct_triage():
    print("Conducting triage...")  # Placeholder

def check_shifts():
    print("Checking shifts...")  # Placeholder

def schedule_appointment():
    print("Scheduling an appointment...")  # Placeholder

def view_scheduled_appointments():
    print("Viewing scheduled appointments...")  # Placeholder

def update_patient_records():
    print("Updating patient records...")  # Placeholder

def log_patient_vitals():
    print("Logging patient vitals...")  # Placeholder

def staff_chat():
    print("Opening staff chat...")  # Placeholder

def run_nurse_portal(nurse):
    print("Welcome, " + nurse.username + "!")
    time.sleep(1)
    view_notifications()
    time.sleep(0.5)
    nurse_dashboard(nurse)  # Call the nurse dashboard function

def main():
    #user login is handled in another file
    username = input("Enter your username: ")  # Get username input from user
    nurse = Nurse(username)  # Create a Nurse object
    nurse.add_patient("John Doe")
    run_nurse_portal(nurse)  # Start the nurse portal with the entered username

if __name__ == "__main__":
    main()  # Run the main function when the script is executed
