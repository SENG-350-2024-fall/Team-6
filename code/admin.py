import time

# Constants
ADMIN_CREDENTIALS = {
    "admin01": "adminpassword1",
    "admin02": "adminpassword2",
}

new_notification = 0
notifications = []

# Sample data for user accounts
USER_ACCOUNTS = {
    "John Doe": {"role": "User", "status": "Active", "permission_level": "Read/Write"},
    "Jane Smith": {"role": "User", "status": "Inactive", "permission_level": "Read"},
}


class SystemAdministrator:
    
    def __init__(self, username):
        self.username = username
        self.admin_level = "Super Admin"
        self.tasks = []

    def add_user_account(self, user, role):
        if user in USER_ACCOUNTS:
            print(f"User {user} already exists.")
        else:
            USER_ACCOUNTS[user] = {"role": role, "status": "Active", "permission_level": "Read"}
            add_notification(f"User {user} has been added with {role} role.")
            print(f"User {user} added successfully.")

    def remove_user_account(self, user):
        if user in USER_ACCOUNTS:
            del USER_ACCOUNTS[user]
            add_notification(f"User {user} has been removed from the system.")
            print(f"User {user} removed successfully.")
        else:
            print(f"User {user} does not exist.")

    def update_user_account(self, user, updates):
        if user in USER_ACCOUNTS:
            USER_ACCOUNTS[user].update(updates)
            add_notification(f"User {user}'s account has been updated.")
            print(f"User {user} updated successfully.")
        else:
            print(f"User {user} does not exist.")

    def maintain_system(self):
        print("System maintenance in progress.")
        self.check_diagnostics()
        self.update_software()

    def check_diagnostics(self):
        print("System diagnostics checked.")

    def update_software(self):
        print("System software updated.")

    def perform_security_check(self):
        print("Performing security check...")
        self.system_audit()

    def system_audit(self):
        print("System audit completed successfully.")

    def __str__(self):
        return f"System Administrator: {self.username}"


def authenticate_admin():
    print("\n--- Admin Login ---")
    while True:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        if ADMIN_CREDENTIALS.get(username) == password:
            print(f"Welcome, {username}!")
            return SystemAdministrator(username)
        else:
            print("Invalid credentials. Please try again.")


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
        '1': view_notifications,
        '2': view_user_accounts,
        '3': lambda: manage_user_accounts(admin),
        '4': admin.maintain_system,
        '5': admin.perform_security_check,
        '6': logout
    }

    while True:
        print(f"\n--- Admin Dashboard for {admin.username} ---")
        print("""\
1.  View Notifications
2.  View User Accounts
3.  Manage User Accounts
4.  Maintain System
5.  Perform Security Check
6.  Logout""")

        choice = input("Select a task (1-6): ").strip()
        if choice == '6':
            if input("Do you want to logout? (y/n): ").strip().lower() == 'y':
                print("Logging out...")
                break
        elif choice in tasks:
            tasks[choice]()
        else:
            print("Invalid selection. Please try again.")
        time.sleep(1)


def view_user_accounts():
    if USER_ACCOUNTS:
        print("\n--- User Accounts ---")
        for user, details in USER_ACCOUNTS.items():
            print(f"User: {user}, Role: {details['role']}, Status: {details['status']}, Permission: {details['permission_level']}")
    else:
        print("No user accounts found.")


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


def run_admin_portal():
    admin = authenticate_admin()
    time.sleep(1)
    view_notifications()
    time.sleep(0.5)
    admin_dashboard(admin)


if __name__ == "__main__":
    run_admin_portal()
