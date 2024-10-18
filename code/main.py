import login

def main():
    while True:
        print(" =============================")
        print("|| Welcome to the ED Portal  ||")
        print(" =============================\n")
        print("Select a Portal based on your Role:\n ")
        print("1. Patient")
        print("2. Doctor")
        print("3. Nurse")
        print("4. ED Staff")
        print("5. System Administrator")
        print("6. Exit\n")

        role = input("Please enter the number corresponding to your Portal:\n")

        if role == '1':
            login.clear_terminal()
            # Prompt credentails and verify user
            print("\nPatient Login Portal\n")
            user = login.login()
            if user and user['role'] == 'patient':
                break
        elif role == '2':
            login.clear_terminal()
            print("\nDoctor Login Portal\n")
            user = login.login()
            # Prompt credentails and verify user
            if user and user['role'] == 'doctor':
                break
        elif role == '3':
            # Prompt credentails and verify user
            login.clear_terminal()
            print("\nNurse Login Portal\n")
            user = login.login()
            if user and user['role'] == 'nurse':
                print("Nurse Portal")
                break
        elif role == '4':
            # Prompt credentails and verify user
            login.clear_terminal()
            print("\nED Staff Login Portal\n")
            user = login.login()
            if user and user['role'] == 'ed_staff':
                break
        elif role == '5':
            # Prompt credentails and verify user
            login.clear_terminal()
            print("\nSystem Administrator Login Portal\n")
            user = login.login()
            if user and user['role'] == 'system_admin':
                break
        elif role == '6':
            print("***** Thank you for using the ED Portal :) *****")
            break
        else:
            print("\n\nInvalid option. Please try again.\n\n")
            continue

if __name__ == "__main__":
    main()
