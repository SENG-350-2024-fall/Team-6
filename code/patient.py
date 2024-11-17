import pandas as pd
from csv import writer
from datetime import date
import warnings
from login import *
from user import *
from triage import *
warnings.filterwarnings("ignore")

tr = Triage()
password = "password"
new_users =[]
signed_in = 0

# Strategy interface
class TriageStrategy:
    # Skeleton method
    def execute(self, patient_data):
        pass


# Concrete strategy for registration
class RegisterForTriage(TriageStrategy):
    
    def __init__(self):
        pass
        
    # Body 1
    def execute(self, patient_data):
        print()
        print("    Virtual Triage Registration   ")
        print("-------------------------------------")
        
        ## Calling Triage Class Function
        tr.perform_triage()
        ##
        
        username = input("Username: ")
        name = input("Full Name: ")
        age = input("Age: ")
        address = input("Address: ")
        phone = input("Phone: ")
        reason = input("Reason: ")
        diagnosed_diseases = input("Diagnosed Diseases: ")
        today = date.today()
        print()
        
        if (len(username) == 0 or len(name) == 0 or len(age) == 0 or len(address) == 0 or len(phone) == 0 \
        or len(reason) == 0 or len(diagnosed_diseases) == 0):
            print("Please Don't Leave Any Field Empty!!\n")
            Patient().initiate_actions()
            return
        
        try:
            data = pd.read_csv("patient.csv")
        except FileNotFoundError:
            print("\nPatients File is Not Found!!\n")
            return
        
        for i in range(len(data)):
            if data["Username"].iloc[i] == username and data["Name"].iloc[i] == name:
                print("\nYou are Already Registered!!\n")
                Patient().initiate_actions()
                return
                
        ## Notifying Patient and Nurse
        tr.notify_patient_nurse()
        ##

        ## Add the new user to the list
        global new_users
        new_users.append((username,name))

        '''
        with open("patient.csv", "a", newline="") as csv_file:
            writer_obj = writer(csv_file)
            writer_obj.writerow(
                [name, age, address, phone, password, username, reason, diagnosed_diseases, today, "NA",tr.get_mode(), tr.get_priority(),"NA"]
            )
        '''
        print("\nYour Request Has Been Submitted!")

        patient_data['triageStatus'] = "Registration Confirmed"


# Concrete strategy for undergoing triage
class UndergoTriage(TriageStrategy):
    # Body 2
    def execute(self, patient_data):
        print()
        print("    Virtual Triage Page   ")
        print("-------------------------------------")

        username = input("Username: ")
        name = input("Full Name: ")

        q1 = input("What are your symptoms?  ")
        q2 = input("How long have you been experiencing them?  ")
        q3 = input("Have you experienced this symptom before?  ")
        q4 = input("Has this issue affected your daily activities or work?  ")
        
        answers = [q1 + " ", q2 + " ", q3 + " ", q4 + " "]
        
        if (len(q1) == 0 or len(q2) == 0 or len(q3) == 0 or len(q4) == 0):
            print("\nPlease Don't Leave Any Answer Empty!!\n")
            Patient().initiate_actions()
            return
        
        try:
            data = pd.read_csv("patient.csv")
        except FileNotFoundError:
            print("\nPatients File is Not Found!!\n")
            return
        
        registered = False
        
        for i in range(len(data)):
            if data["Username"].iloc[i] == username and data["Name"].iloc[i] == name:
                
                data["Answers"].iloc[i] = answers
                data["Priority"].iloc[i] = tr.get_priority()
                data["Mode"].iloc[i] = tr.get_mode()
                data["Nurse"].iloc[i] = tr.get_nurse_info()['Name']

                # Write to CSV file
                data.to_csv("patient.csv", sep=",", index=False, encoding="utf-8")
                
                print("\nAnswers Are Saved Successfully!\n")
                registered = True
                break
            
        if registered == False:

            global new_users
            # Simulate answer storage for newly added/registered users
            for usn, n in new_users:
                if (usn == username and n == name):
                    print("\nAnswers Are Saved Successfully!\n")
                    return

            print("\nPlease Register for the Triage First!\n")
            Patient().initiate_actions()
            return
        else:
            patient_data['status'] = "Triage is taken."

class UpdarInfo:

    def __init__(self):
        pass

    def update_usename(self):
        username = input("\nPlease Input Your New Username:  \n")
        return username
    def update_password(self):
        passw = input("\nPlease Input Your New Password:  \n")
        return passw
    def update_phone_number(self):
        phone_num = input("\nPlease Input Your New Phone#:  \n")
        return phone_num
    def update_mailing_address(self):
        mailing_address = input("\nPlease Input Your New Mailing Address:  \n")
        return mailing_address
    def update_age(self):
        age = input("\nPlease Input Your New Age:  \n")
        return age
    
# Context for the patient
class Patient:
    def __init__(self):
        self.patient_data = {
            "status": "Triage is Not Taken",
            "triageStatus": "Idle"
        }
        self.strategy = None

    def check_patient_status(self):
        
        status = input("Please Input Your Status: 1 = New Patient,  2 = Registered Patient  ")
        
        all_users = {}
        user_new = None

        if status == "1":
            ##Testing           
            username = input("Please Input Your Username: ")
            password = input("Please Input Your Password: ")
            name = input("Please Input Your Full Name: ")
            address = input("Please Input Your Address: ")
            age = input("Please Input Your Age: ")
            phone = input("Please Input Your Phone#: ")

            user_factory = UserLoader.role_factory_map.get("patient")
            user_new = user_factory.create_user(
                name,
                age,
                address,
                phone,
                username,
                password
            )

            ## Users_patients list from users.py
            users_patients.append(user_new)
            UserLoader.load_all_users()

            return
           
        elif status == "2":

            print("\nPlease Login First\n")
            login("patient")

            ## Accessing login_check from login.py
            if get_invalid_login() == 1:
               self.check_patient_status() 
            
        else:
            print("\nInvalid Input!!\n")
            self.check_patient_status()
            return

    def set_strategy(self, strategy: TriageStrategy):
        self.strategy = strategy

    def execute_strategy(self):
        if self.strategy:
            self.strategy.execute(self.patient_data)

    def initiate_actions(self):
        print()

        global signed_in

        if signed_in == 0:
            self.check_patient_status()
        signed_in = 1
    
        print("\n")
        print("       Patient Welcome Page          ")
        print("-------------------------------------")
        op = input("Choose an Option:\n\n 1 = Register for Triage\n 2 = Undergo Triage\n 3 = Update Username\n 4 = Update Password\n 5 = Update Phone Number\n 6 = Update Mailing Address\n 7 = Update Age \n 8 = Exit\n\n ")

        if op == "1":
            self.set_strategy(RegisterForTriage())
        elif op == "2":
            self.set_strategy(UndergoTriage())
        elif op == "3":
            UpdarInfo().update_usename()
            print("Username Has Been Updated!\n\n")
            self.initiate_actions()
        elif op == "4":
            UpdarInfo().update_password()
            print("Password Has Been Updated!\n\n")
            self.initiate_actions()           
        elif op == "5":
            UpdarInfo().update_phone_number()
            print("Phone Number Has Been Updated!\n\n")
            self.initiate_actions()
        elif op == "6":
            UpdarInfo().update_mailing_address()
            print("Mailing Address Has Been Updated!\n\n")
            self.initiate_actions()
        elif op == "7":
            UpdarInfo().update_age()
            print("Age Has Been Updated!\n\n")
            self.initiate_actions()
        elif op == "8":
            signed_in = 0
            return
        else:
            print("Please Pick a Valid Input!!")
            self.initiate_actions()
            return

        self.execute_strategy()


'''
if __name__ == "__main__":
    patient_instance = Patient()
    patient_instance.initiate_actions()
'''
