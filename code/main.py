# main.py

'''import patient
import doctor
import nurse
import ed_staff
import system_admin
'''
def main():
    while(True):
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
            #patient.run_patient_portal()
            print("Patient Portal")
            break
        elif role == '2':
            #doctor.run_doctor_portal()
            print("Doctor Portal")
            break
        elif role == '3':
            #nurse.run_nurse_portal()
            print("Nurse Portal")
            break
        elif role == '4':
            #ed_staff.run_ed_staff_portal()
            print("ED Staff Portal")
            break
        elif role == '5':
            #system_admin.run_system_admin_portal()
            print("System Administrator Portal")
            break
        elif role == '6':
            #system_admin.run_system_admin_portal()
            print("***** Thank you for using the ED Portal :) *****")
            break
        else:
            print("\n\nInvalid option. Please try again.\n\n")
            continue


if __name__ == "__main__":
    main()
