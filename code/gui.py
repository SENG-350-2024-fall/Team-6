import login  # Import your login module
import doctor_dashboard
import nurse_dashboard
import admin
import ed_staff_dashboard
import patient

def role_login(portal_name, dashboard, user):
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

def main():
    """
    Main function to display role selection and handle login and dashboard access.
    """
    roles = {
        '1': ('Patient', "Patient Dashboard"),
        '2': ('Doctor', doctor_dashboard.doctor_dashboard),
        '3': ('Nurse', nurse_dashboard.run_nurse_portal),
        '4': ('ED Staff', ed_staff_dashboard.ed_staff_dashboard),
        '5': ('System Administrator', admin.run_admin_portal),
    }

    while True:
        print(" =============================")
        print("|| Welcome to the ED Portal  ||")
        print(" =============================\n")
        print("Select a Portal based on your Role:\n")
        for num, (name, _) in roles.items():
            print(f"{num}. {name}")
        print("6. Exit\n")

        role_choice = input("Please enter the number corresponding to your Portal:\n")

        if role_choice == '6':
            print("***** Thank you for using the ED Portal :) *****")
            break
        elif role_choice in roles:
            portal, dashboard = roles[role_choice]
            user = login.login(portal.lower().replace(" ", "_"))  # Prompt user to log in
            if user:
                role_login(portal, dashboard, user)
            else:
                print("Invalid login or role mismatch. Please try again.\n")
        else:
            print("\n\nInvalid option. Please try again.\n\n")

if __name__ == "__main__":
    main()
