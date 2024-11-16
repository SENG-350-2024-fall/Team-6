import time
import os
from user import SystemAdmin
from data_stores import all_users
import pandas as pd
from user import UserLoader
from notification import Notification, notify_action, Observer
from user import DoctorFactory,PatientFactory,NurseFactory,SystemAdminFactory,EdStaffFactory


new_notification = 0
notifications = []

# Sample data for user accounts
USER_ACCOUNTS = {
    "John Doe": {"role": "User", "status": "Active", "permission_level": "Read/Write"},
    "Jane Smith": {"role": "User", "status": "Inactive", "permission_level": "Read"},
}

def terminal_clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class SystemAdministrator(SystemAdmin):
    
    def __init__(self, username, name):
        super().__init__(name, 0, '', '', username, 'password')
        self.admin_level = "Super Admin"

    def add_user_account(self, name, role):
        
        user_factory_doctor = DoctorFactory()
        user_factory_patient = PatientFactory()
        user_factory_admin = SystemAdminFactory()
        user_factory_edstaff = EdStaffFactory()
        user_factory_nurse = NurseFactory()

        if role == 'doctor':
            age = input("Enter Age: ").strip()
            address = input("Enter Address: ")
            phone = input("Enter Phone Number: ").strip()
            username = input("Enter the Username: ").strip()
            password = input("Enter Password: ").strip()
            spec = input("Enter Specialization: ").strip()
            avail = input("Enter Availibility: ").strip()

            new_user = user_factory_doctor.create_user(name,age,address,phone,username,password,spec,avail)
        elif role == 'patient':
            age = input("Enter Age: ").strip()
            address = input("Enter Address: ")
            phone = input("Enter Phone Number: ").strip()
            username = input("Enter the Username: ").strip()
            password = input("Enter Password: ").strip()
            new_user = user_factory_patient.create_user(name,age,address,phone,username,password)
        elif role== 'system_administrator':
            age = input("Enter Age: ").strip()
            address = input("Enter Address: ")
            phone = input("Enter Phone Number: ").strip()
            username = input("Enter the Username: ").strip()
            password = input("Enter Password: ").strip()
            new_user = user_factory_admin.create_user(name,age,address,phone,username,password)
        elif role == 'ed_staff':
            age = input("Enter Age: ").strip()
            address = input("Enter Address: ")
            phone = input("Enter Phone Number: ").strip()
            username = input("Enter the Username: ").strip()
            password = input("Enter Password: ").strip()
            new_user = user_factory_edstaff.create_user(name,age,address,phone,username,password)
        elif role == 'nurse':
            age = input("Enter Age: ").strip()
            address = input("Enter Address: ")
            phone = input("Enter Phone Number: ").strip()
            username = input("Enter the Username: ").strip()
            password = input("Enter Password: ").strip()
            avail = input("Enter Availibility (yes/no): ").strip().lower() == 'yes'
            triage = input("Enter whether Triage Ready or Not (yes/no): ").strip().lower() == 'yes'
            assigned_patients = input("Enter Assigned Patients (seperated by ,) or press enter to it blank: ").split(',')
            notifications = input("Enter notification or press enter to it blank: ").strip()
            shift = input("Enter Shift (Day/Night/Evening): ").strip()

            assigned_patients = [patient.strip() for patient in assigned_patients if patient.strip()]

            new_user = user_factory_nurse.create_user(name,age,address,phone,username,password,avail,triage,assigned_patients,notifications,shift)


        all_users[role].append(new_user)

        if new_user in all_users[role]:
            print(f"User '{new_user.name}' successfully added to role '{role}'.")
            print(f"Please go to View User Accounts and select {role} to view updated user account list.")
            input("\nPress Enter to go back to the Dashboard...")
           

        
    def remove_user_account(self, name, username,role):

        remove_user = None
        for curr in all_users[role]:
            if curr.name == name and curr.username == username:
                remove_user = curr
                break

        if remove_user:
            all_users[role].remove(remove_user)
            print(f"User '{name}' removed successfully from role '{role}'.")
            print(f"Please go to View User Accounts and select {role} to view updated user account list.")
            input("\nPress Enter to go back to the Dashboard...")
        


    def update_user_account(self, name, username,role):
        
        user_to_update = None

        for user in all_users[role]:
            if user.username == username:
                user_to_update = user
                print(user_to_update.name)
                break

        
        # Prompt for each specific attribute
        age = input(f"Enter new Age (current: '{user_to_update.age}'): ").strip()
        if age:
            user_to_update.age = age

        address = input(f"Enter new Address (current: '{user_to_update.address}'): ").strip()
        if address:
            user_to_update.address = address

        phone = input(f"Enter new Phone Number (current: '{user_to_update.phone_number}'): ").strip()
        if phone:
            user_to_update.phone_number = phone

        password = input(f"Enter new Password (current: '{user_to_update.password}'): ").strip()
        if password:
            user_to_update.password = password

        if role == "doctor":
            avail = input("Enter Availibility (yes/no): ").strip().lower() == 'yes'
            if avail:
                user_to_update.available = avail
            spec = input("Enter Specialization: ").strip()
            if spec:
                user_to_update.specialization = spec
        
        if role == "nurse":
            avail = input("Enter Availibility (yes/no): ").strip().lower() == 'yes'
            if avail:
                user_to_update.available = avail
            triage = input("Enter Traige Ready (yes/no): ").strip().lower() == 'yes'
            if triage:
                user_to_update.triage_ready = triage
            shifts = input("Enter Shift (Day/Night/Evening): ").strip()
            if shifts:
                user_to_update.shift = shifts
            assigned_patient = input("Enter Assigned Patients (seperated by ,) or press enter to it blank: ").split(',')
            assigned_patient = [patient.strip() for patient in assigned_patient if patient.strip()]
            if assigned_patient:
                user_to_update.assigned_patients = assigned_patient

        print(f"User '{name}' updated successfully from role '{role}'.")
        print(f"Please go to View User Accounts and select {role} to view updated user account list.")
        input("\nPress Enter to go back to the Dashboard...")
        
            


    def maintain_system(self):
        print("System maintenance in progress.")
        self.check_diagnostics()
        self.update_software()

    def check_diagnostics(self):
        print("Running System diagnostics test.....")
        time.sleep(2)
        print("Please wait...")
        time.sleep(2)
        print("System diagnostics checked.")

    def update_software(self):
        print("Checking for software updates....")
        time.sleep(2)
        print("System software is already updated.")
        time.sleep(2)
        input("\nPress Enter to go back to the Dashboard...")


    def perform_security_check(self):
        print("Starting security check...")
        time.sleep(2)
        print("Checking firewall status...")
        time.sleep(2)
        print("Firewall status: Active")
    
        print("Scanning for vulnerabilities...")
        time.sleep(2)
        print("Vulnerabilities found: None")
    
        print("Verifying user access permissions...")
        time.sleep(2)
        print("All user permissions are correctly configured.")
        time.sleep(2)
        print("Security check complete. Proceeding to system audit...")
        self.system_audit()

    def system_audit(self):
        print("Starting system audit...")
        time.sleep(2)
        print("Analyzing system logs for unusual activity...")
        time.sleep(2)
        print("No unusual activity found in system logs.")
        time.sleep(2)
        print("Checking for outdated software...")
        time.sleep(2)
        print("All software is up-to-date.")
        time.sleep(2)
        print("Validating data integrity across all databases...")
        time.sleep(2)
        print("Data integrity check passed successfully.")
        time.sleep(2)
        print("System audit completed successfully.")
        time.sleep(2)
        input("\nPress Enter to go back to the Dashboard...")

    def __str__(self):
        return f"System Administrator: {self.username}"


def view_notifications():
    global new_notification
    if notifications:
        print(f"\nYou have {new_notification} new notification(s)")
        print("\n--- Notifications ---")
        for i, notification in enumerate(notifications, 1):
            print(f"{i}. {notification}")
    else:
        print("\nYou have no new notifications.")

    if input("Clear notifications? (y/n): ").strip().lower() == 'y':
        clear_notifications()
    
    


def add_notification(message):
    global new_notification
    notifications.append(message)
    new_notification += 1


def clear_notifications():
    global new_notification
    notifications.clear()
    new_notification = 0
    print("All notifications cleared!")


def admin_dashboard(admin):
    tasks = {
        '1': admin.notifications.view_notifications,
        '2': view_user_accounts,
        '3': lambda: manage_user_accounts(admin),
        '4': admin.maintain_system,
        '5': admin.perform_security_check,
        '6': logout
    }

    while True:
        terminal_clear()
        print(f"\n Welcome {admin.name} ")
        time.sleep(1)
        terminal_clear()
        print(" =============================")
        print(f"|| {admin.name}'s Dashboard ||")
        print(" =============================\n")
        print("Please select an option:\n")
        print("""\
1.  View Notifications
2.  View User Accounts
3.  Manage User Accounts
4.  Maintain System
5.  Perform Security Check
6.  Logout""")

        choice = input("Enter the number corresponding to your choice: ").strip()
        if choice == '6':
            if input("Do you want to logout? (y/n): ").strip().lower() == 'y':
                print("Logging out...")
                return False
        elif choice in tasks:
            tasks[choice]()
        else:
            print("Invalid selection. Please try again.")
            time.sleep(5)


def view_user_accounts():
    terminal_clear()
    print("Different User Types:\n")
    print("""\
1.  Doctors
2.  Patients
3.  Nurse
4.  ED Staff
5.  System Admin""")
    
    user_type = input("\nPlease enter the number corresponding to the to type of user account you want to see: ").strip()
    roles = {
        "1": "doctor",
        "2": "patient",
        "3": "nurse",
        "4": "ed_staff",
        "5": "system_administrator"
    }

    role_selected = roles.get(user_type)
    if not role_selected:
        print("Invalid selection. Please try again.")
        return
    
    table_data = []
    
    if role_selected and all_users:
        terminal_clear()
        print(f"\n|| All {role_selected.capitalize()} Accounts ||\n")

        for usertype in all_users[role_selected]:
            userdata = {
                "Name": usertype.name,
                "Age": usertype.age,
                "Address": usertype.address,
                "Phone Number": usertype.phone_number,
                "Username": usertype.username,
                "Password": usertype.password
            }
            
            if role_selected=="doctor":
                userdata["Specialization"] = usertype.specialization
                userdata["Availability"] = usertype.available
            elif role_selected=="nurse":
                userdata["Availability"] = usertype.available
                userdata["Triage Ready"] = usertype.triage_ready
                userdata["Patients Assigned"] = usertype.assigned_patients if usertype.assigned_patients else "N/A"
                userdata["Notifications"] = [notif["message"] for notif in usertype.notifications.notifications] if [notif["message"] for notif in usertype.notifications.notifications] else "N/A"
                userdata["Shifts"] = usertype.shift
                userdata["Vitals"] = usertype.vitals_dict if usertype.vitals_dict else "N/A"
                
            table_data.append(userdata)

        df = pd.DataFrame(table_data)
        print(df.to_string(index=False))
        input("\nPress Enter to go back to the Dashboard...")
               

def manage_user_accounts(admin):
    print("\n--- Manage User Accounts ---")
    print("Choose one of the following action's: ")
    print("""\
1.  add
2.  remove
3.  update""")
    action = input("\nPlease enter the number corresponding to the to type of user account you want to see: ").strip()
    actions = {
        "1": "add",
        "2": "remove",
        "3": "update",
    }

    action_selected = actions.get(action)
    print(action_selected)
    if action_selected == 'add':
        user = input("Enter the user's name: ").strip()
        print("Different role Types:\n")
        print("""\
    1.  Doctors
    2.  Patients
    3.  Nurse
    4.  ED Staff
    5.  System Admin""")
        
        roles = {
        "1": "doctor",
        "2": "patient",
        "3": "nurse",
        "4": "ed_staff",
        "5": "system_administrator"
    }
        role_type = input("Enter the user's role: ").strip().lower()
        role_selected = roles.get(role_type)
        admin.add_user_account(user, role_selected)
    elif action_selected == 'update':
        name = input("Enter the user's current name: ").strip()
        username = input("Enter user's current username: ").strip()
        print("Different role Types:\n")
        print("""\
    1.  Doctors
    2.  Patients
    3.  Nurse
    4.  ED Staff
    5.  System Admin""")
        
        roles = {
        "1": "doctor",
        "2": "patient",
        "3": "nurse",
        "4": "ed_staff",
        "5": "system_administrator"
    }
        role_type = input("Enter the user's role: ").strip().lower()
        role_selected = roles.get(role_type)

        admin.update_user_account(name,username,role_selected)
    elif action_selected == 'remove':
        name = input("Enter the user's name: ").strip()
        username = input("Enter username: ").strip()
        print("Different role Types:\n")
        print("""\
    1.  Doctors
    2.  Patients
    3.  Nurse
    4.  ED Staff
    5.  System Admin""")
        
        roles = {
        "1": "doctor",
        "2": "patient",
        "3": "nurse",
        "4": "ed_staff",
        "5": "system_administrator"
    }
        role_type = input("Enter the user's role: ").strip().lower()
        role_selected = roles.get(role_type)
        admin.remove_user_account(name,username,role_selected)
    else:
        print("Invalid action. Please try again.")


def logout():
    print("Logged out successfully.")


def run_admin_portal(user):
    admin = SystemAdministrator(user.username,user.name)
    admin_dashboard(admin)


if __name__ == "__main__":
    run_admin_portal()
