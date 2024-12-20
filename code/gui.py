# gui.py
import threading
import login  # Import your login module
import doctor_dashboard
import nurse_dashboard
import admin
import ed_staff_dashboard
import patient
from heartbeat import heartbeat

class GUI:
    def __init__(self):
        # Define the roles and corresponding dashboards
        self.roles = {
            '1': ('Patient', lambda pat: patient.Patient().initiate_actions()),
            '2': ('Doctor', doctor_dashboard.doctor_dashboard),
            '3': ('Nurse', nurse_dashboard.run_nurse_portal),
            '4': ('ED Staff', ed_staff_dashboard.ed_staff_dashboard),
            '5': ('System Administrator', lambda user: admin.run_admin_portal(user)),
        }

    def role_login(self, portal_name, dashboard, user):
        """
        Clears the terminal and displays the login portal for the specified role.
        If a dashboard function is provided, it calls that dashboard after login.
        """
        login.clear_terminal()
        print(f"\n{portal_name} Login Portal\n")
        if user and dashboard:
            dashboard(user)
        else:
            print(f"Welcome to the {portal_name} Portal!")

    def main(self):
        """
        Main function to display role selection and handle login and dashboard access.
        """
        while True:
            print(" =============================")
            print("|| Welcome to the ED Portal  ||")
            print(" =============================\n")
            print("Select a Portal based on your Role:\n")
            for num, (name, _) in self.roles.items():
                print(f"{num}. {name}")
            print("6. Exit\n")

            role_choice = input("Please enter the number corresponding to your Portal:\n")

            if role_choice == '6':
                print("***** Thank you for using the ED Portal :) *****")
                break
            elif role_choice in self.roles:
                portal, dashboard = self.roles[role_choice]
                
                if role_choice != "1":
                    user = login.login(portal.lower().replace(" ", "_"))  # Prompt user to log in

                    if user is not None:
                        self.role_login(portal, dashboard, user)
                    else:
                        print("Invalid login or role mismatch. Please try again.\n")
                else:
                    patient.Patient().initiate_actions()
            else:
                print("\n\nInvalid option. Please try again.\n\n")


if __name__ == "__main__":
    heartbeat_thread = threading.Thread(target=heartbeat, args=(10,), daemon=True)
    heartbeat_thread.start()
    gui = GUI()
    gui.main()
