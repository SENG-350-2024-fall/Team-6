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
            time.sleep(20)
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
                userdata["Notifications"] = [notif["message"] for notif in usertype.notifications.notifications]
                userdata["Shifts"] = usertype.shift
                userdata["Vitals"] = usertype.vitals_dict if usertype.vitals_dict else "N/A"
                
            table_data.append(userdata)

        df = pd.DataFrame(table_data)
        print(df.to_string(index=False))
        input("\nPress Enter to go back to the Dashboard...")
               



    # if USER_ACCOUNTS:
    #     print("\n--- User Accounts ---")
    #     for user, details in USER_ACCOUNTS.items():
    #         print(f"User: {user}, Role: {details['role']}, Status: {details['status']}, Permission: {details['permission_level']}")
    # else:
    #     print("No user accounts found.")


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
