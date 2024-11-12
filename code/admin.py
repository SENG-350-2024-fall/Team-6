import time
import os
from user import SystemAdmin
from data_stores import all_users
import pandas as pd
from notification import Notification, notify_action, Observer

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

    def add_user_account(self, user, role):
        if user in USER_ACCOUNTS:
            print(f"User {user} already exists.")
        else:
            USER_ACCOUNTS[user] = {"role": role, "status": "Active", "permission_level": "Read"}
            self.notifications.add_notification(f"User {user} has been added with {role} role.")

    def remove_user_account(self, user):
        if user in USER_ACCOUNTS:
            del USER_ACCOUNTS[user]
            self.notifications.add_notification(f"User {user} has been removed from the system.")
            print(f"User {user} removed successfully.")
        else:
            print(f"User {user} does not exist.")

    def update_user_account(self, user, updates):
        if user in USER_ACCOUNTS:
            USER_ACCOUNTS[user].update(updates)
            self.notifications.add_notification(f"User {user}'s account has been updated.")
            print(f"User {user} updated successfully.")
        else:
            print(f"User {user} does not exist.")

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
            time.sleep(100)
        else:
            print("Invalid selection. Please try again.")
            time.sleep(5)
        # time.sleep(30)


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
        "4": "EDStaff",
        "5": "SystemAdmin"
    }

    role_selected = roles.get(user_type)
    print(role_selected)
    if not role_selected:
        print("Invalid selection. Please try again.")
        return
    
    table_data = []

    if role_selected in all_users and all_users[role_selected]:
        print(f"\n|| All {role_selected.capitalize()} Accounts ||\n")

        # Prepare table data for the selected role
        table_data = []
        for usertype in all_users[role_selected]:
            userdata = {
                "Name": usertype.name,
                "Age": usertype.age,
                "Address": usertype.address,
                "Phone Number": usertype.phone_number,
                "Username": usertype.username,
                "Password": usertype.password
            }

            # Add role-specific attributes
            if role_selected == "doctor":
                userdata["Specialization"] = usertype.specialization
                userdata["Availability"] = usertype.available
            elif role_selected == "nurse":
                userdata["Availability"] = usertype.available
                userdata["Triage Ready"] = usertype.triage_ready
                userdata["Patients Assigned"] = usertype.assigned_patients if usertype.assigned_patients else "N/A"
                userdata["Notifications"] = [notif["message"] for notif in usertype.notifications.notifications]
                userdata["Shifts"] = usertype.shift
                userdata["Vitals"] = usertype.vitals_dict if usertype.vitals_dict else "N/A"
            elif role_selected == "patient":
                userdata["Status"] = usertype.status
            elif role_selected == "system_administrator":
                userdata["Admin Level"] = usertype.admin_level
            elif role_selected == "ed_staff":
                # Add any specific fields for EdStaff if needed
                pass

            table_data.append(userdata)

        # Convert to DataFrame for a formatted table view
        df = pd.DataFrame(table_data)
        print(df.to_string(index=False))




    
    # if role_selected and all_users:
    #     # terminal_clear()
    #     userdata = {}

    #     # for doctor in all_users["doctor"]:
    #     #     print(f"Name: {doctor.name}, Age: {doctor.age}, Specialization: {doctor.specialization}, Availability: {doctor.available}")

    #     # if role_selected=="doctor":
    #     #     for doctor in all_users['doctor']:
    #     #         if isinstance(doctor,Doctor):
    #     #             userdata["Name"] = doctor.name
    #     #             userdata["Age"] = doctor.age
    #     #             userdata["Address"] = doctor.address
    #     #             userdata["Phone Number"] = doctor.phone_number
    #     #             userdata["Username"] = doctor.username
    #     #             userdata["Password"] = doctor.password
    #     #             userdata["Specialization"] = doctor.specialization
    #     #             userdata["Availability"] = doctor.available
    #     #             table_data.append(userdata)

        
    #     # print(f"\n|| All {role_selected.capitalize()} Accounts ||\n")

    #     # for usertype in all_users[role_selected]:
    #         # print(f"User type: {type(user)}")  # Debugging line to confirm the object type
            
    #         # Basic user details
    #         # print(f"Name: {user.name}")

    #         # Role-specific details
    #         # if role_selected == "doctor" and isinstance(usertype, Doctor):
    #         #     # Ensure we only try to access Doctor-specific attributes for Doctor objects
    #         #     print(f"Specialization: {usertype.specialization}, Availability: {usertype.available}")
    #         #     userdata["Name"] = usertype.name
    #         #     userdata["Age"] = usertype.age
    #         #     userdata["Address"] = usertype.address
    #         #     userdata["Phone Number"] = usertype.phone_number
    #         #     userdata["Username"] = usertype.username
    #         #     userdata["Password"] = usertype.password
    #         #     userdata["Specialization"] = usertype.specialization
    #         #     userdata["Availability"] = usertype.available
    #         #     table_data.append(userdata)
                
    #         # else:
    #         #     pass
    #         # if role_selected == "patient" and isinstance(usertype, Patient):
    #         #     # Patient-specific fields if any
    #         #     # print(f"Status: {user.status}")
    #         #     userdata["Name"] = usertype.name
    #         #     userdata["Age"] = usertype.age
    #         #     userdata["Address"] = usertype.address
    #         #     userdata["Phone Number"] = usertype.phone_number
    #         #     userdata["Username"] = usertype.username
    #         #     userdata["Password"] = usertype.password
    #         #     table_data.append(userdata)

    #         # else:
    #         #     pass

    #         # if role_selected == "nurse" and isinstance(usertype, Nurse):
    #         #     # Nurse-specific fields
    #         #     # print(f"Shift: {user.shift}")
    #         #     userdata["Name"] = usertype.name
    #         #     userdata["Age"] = usertype.age
    #         #     userdata["Address"] = usertype.address
    #         #     userdata["Phone Number"] = usertype.phone_number
    #         #     userdata["Username"] = usertype.username
    #         #     userdata["Password"] = usertype.password
    #         #     userdata["Availability"] = usertype.available
    #         #     userdata["Triage Ready"] = usertype.triage_ready
    #         #     userdata["Patients Assigned"] = usertype.assigned_patients if usertype.assigned_patients else "N/A"
    #         #     userdata["Notifications"] = [notif["message"] for notif in usertype.notifications.notifications]
    #         #     userdata["Shifts"] = usertype.shift
    #         #     userdata["Vitals"] = usertype.vitals_dict if usertype.vitals_dict else "N/A"
    #         # else:
    #         #     pass
    #         # if role_selected == "system_administrator" and isinstance(usertype, SystemAdmin):
    #         #     # SystemAdmin-specific fields
    #         #     userdata["Name"] = usertype.name
    #         #     userdata["Age"] = usertype.age
    #         #     userdata["Address"] = usertype.address
    #         #     userdata["Phone Number"] = usertype.phone_number
    #         #     userdata["Username"] = usertype.username
    #         #     userdata["Password"] = usertype.password
    #         # else:
    #         #     pass
    #         # if role_selected=="ed_staff" and isinstance(user_type,EdStaff):
    #         #     userdata["Name"] = usertype.name
    #         #     userdata["Age"] = usertype.age
    #         #     userdata["Address"] = usertype.address
    #         #     userdata["Phone Number"] = usertype.phone_number
    #         #     userdata["Username"] = usertype.username
    #         #     userdata["Password"] = usertype.password

           



    #     for usertype in all_users[role_selected]:
    #         print(usertype)
    #     #     userdata = {
    #     #         "Name": usertype.name,
    #     #         "Age": usertype.age,
    #     #         "Address": usertype.address,
    #     #         "Phone Number": usertype.phone_number,
    #     #         "Username": usertype.username,
    #     #         "Password": usertype.password
    #     #     }

    #     #     if role_selected == "doctor" and isinstance(usertype):
    #     # # Access only Doctor-specific details
    #     #         userdata["Specialization"] = usertype.specialization
    #     #         userdata["Availability"] = usertype.available
            
            
    #         if role_selected == "doctor":
    #              if hasattr(usertype, "name"):
    #                  userdata["Name"] = usertype.name
    #              if hasattr(usertype, "Age"):
    #                  userdata["Age"] = usertype.age
    #              if hasattr(usertype, "address"):
    #                  userdata["Address"] = usertype.address
    #              if hasattr(usertype, "phone_number"):
    #                  userdata["Phone Number"] = usertype.phone_number
    #              if hasattr(usertype, "username"):
    #                  userdata["Username"] = usertype.username
    #              if hasattr(usertype, "password"):
    #                  userdata["Password"] = usertype.password
    #              if hasattr(usertype, "specialization"):
    #                  userdata["Specialization"] = usertype.specialization
    #              if hasattr(usertype, "available"):
    #                 userdata["Availability"] = usertype.available
    #         table_data.append(userdata)

    #     #         # userdata["Specialization"] = usertype.specialization
    #     #         # userdata["Availability"] = usertype.available
    #     #     elif role_selected == "nurse":

    #     #         if hasattr(usertype, "name"):
    #     #              userdata["Name"] = usertype.name
    #     #         if hasattr(usertype, "Age"):
    #     #              userdata["Age"] = usertype.age
    #     #         if hasattr(usertype, "address"):
    #     #             userdata["Address"] = usertype.address
    #     #         if hasattr(usertype, "phone_number"):
    #     #              userdata["Phone Number"] = usertype.phone_number
    #     #         if hasattr(usertype, "username"):
    #     #              userdata["Username"] = usertype.username
    #     #         if hasattr(usertype, "password"):
    #     #              userdata["Password"] = usertype.password
    #     #         if hasattr(usertype, "available"):
    #     #              userdata["Availability"] = usertype.available
    #     #         if hasattr(usertype, "triage_ready"):
    #     #              userdata["Triage Ready"] = usertype.triage_ready
    #     #         if hasattr(usertype, "assigned_patients"):
    #     #              userdata["Patients"] = usertype.assigned_patients
    #     #         if hasattr(usertype, "notifications"):
    #     #              userdata["Notifications"] = [notif["message"] for notif in getattr(usertype.notifications, "notifications", "N/A")]
    #     #         if hasattr(usertype, "shift"):
    #     #              userdata["Shifts"] = usertype.shift
    #     #         if hasattr(usertype, "vitals_dict"):
    #     #              userdata["Vitals"] = usertype.vitals_dict

    #     #         # userdata["Availability"] = getattr(usertype, "available", "N/A")
    #     #         # userdata["Triage Ready"] = getattr(usertype, "triage_ready", "N/A")
    #     #         # userdata["Patients Assigned"] = getattr(usertype, "assigned_patients", "N/A")
    #     #         # userdata["Notifications"] = [notif["message"] for notif in getattr(usertype.notifications, "notifications", "N/A")]
    #     #         # userdata["Shifts"] = getattr(usertype, "shift", "N/A")
    #     #         # userdata["Vitals"] = getattr(usertype, "vitals_dict", "N/A")
    #     #     elif role_selected == "patient":
    #     #         # Patient-specific fields can be added here if necessary
    #     #         pass
    #     #     elif role_selected == "ed_staff" or role_selected == "system_administrator":
    #     #         # Fields for other roles can be handled here as needed
    #     #         pass
                
             

        # df = pd.DataFrame(table_data)
        # # df.dropna(inplace=True)
        # print(df.to_string(index=False))
        # input("\nPress Enter to go back to the Dashboard...")
               



def manage_user_accounts(admin):
    print("\n--- Manage User Accounts ---")
    action = input("Enter action (add/update/remove): ").strip().lower()
    user = input("Enter the user's name: ").strip()

    if action == 'add':
        role = input("Enter the user's role: ").strip()
        admin.add_user_account(user, role)
    elif action == 'update':
        updates = {}
        role = input("Enter new role (leave blank to skip): ").strip()
        if role:
            updates["role"] = role
        status = input("Enter new status (Active/Inactive): ").strip()
        if status:
            updates["status"] = status
        admin.update_user_account(user, updates)
    elif action == 'remove':
        admin.remove_user_account(user)
    else:
        print("Invalid action. Please try again.")


def logout():
    print("Logged out successfully.")


def run_admin_portal(user):
    admin = SystemAdministrator(user.username,user.name)
    admin_dashboard(admin)


if __name__ == "__main__":
    run_admin_portal()
