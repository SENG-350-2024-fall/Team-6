import login
import doctor_dashboard
import nurse
import admin

def role_login(portal_name, dashboard=None):
    login.clear_terminal()
    print(f"\n{portal_name} Login Portal\n")
    if dashboard:
        dashboard()
    else:
        print(f"Welcome to the {portal_name} Portal!")


def main():
    roles = {
        '1': ('Patient', None),
        '2': ('Doctor', doctor_dashboard.doctor_dashboard),
        '3': ('Nurse', nurse.run_nurse_portal),
        '4': ('ED Staff', None),
        '5': ('System Administrator', admin.run_admin_portal),
    }
    while True:
        print(" =============================")
        print("|| Welcome to the ED Portal  ||")
        print(" =============================\n")
        print("Select a Portal based on your Role:\n ")
        for num, (name, dashboard) in roles.items():
            print(f"{num}. {name}")
        print("6. Exit\n")

        role = input("Please enter the number corresponding to your Portal:\n")

        if role == '6':
            print("***** Thank you for using the ED Portal :) *****")
            break
        elif role in roles:
            portal, dashboard = roles[role]
            user = login.login()
            if user and user['role'].lower() == portal.lower():
                role_login(portal, dashboard)
                break
            else: 
                print('Invalid login. Please try again \n')
        else:
            print("\n\nInvalid option. Please try again.\n\n")

if __name__ == "__main__":
    main()