import pandas as pd
from csv import writer
from datetime import date
import warnings
from triage import *
warnings.filterwarnings("ignore")

tr = Triage()
password = "password"

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
        
        ## Calling Triage Class Fucntion
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
            return
        
        try:
            data = pd.read_csv("patient.csv")
        except FileNotFoundError:
            print("\nPatients File is Not Found!!\n")
            return
        
        for i in range(len(data)):
            if data["Username"].iloc[i] == username and data["Name"].iloc[i] == name:
                print("You are Already Registered!!")
                exit(0)
                
        ## Notifying Patient and Nurse
        tr.notify_patient_nurse()
        ##
        
        with open("patient.csv", "a", newline="") as csv_file:
            writer_obj = writer(csv_file)
            writer_obj.writerow(
                [name, age, address, phone, password, username, reason, diagnosed_diseases, today, "NA",tr.get_mode(), tr.get_priority(),"NA"]
            )
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
            print("Please Don't Leave Any Answer Empty!!")
            return
        
        try:
            data = pd.read_csv("patient.csv")
        except FileNotFoundError:
            print("\nPatients File is Not Found!!")
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
                
                print("\nAnswers Are Saved Successfully!")
                registered = True
                break
            
        if registered == False:
            print("\nPlease Register for the Triage First!")
        else:
            patient_data['status'] = "Triage is taken."
        


# Context for the patient
class Patient:
    def __init__(self):
        self.patient_data = {
            "status": "Triage is Not Taken",
            "triageStatus": "Idle"
        }
        self.strategy = None

    def set_strategy(self, strategy: TriageStrategy):
        self.strategy = strategy

    def execute_strategy(self):
        if self.strategy:
            self.strategy.execute(self.patient_data)

    def initiate_actions(self):
        print()
        print("       Patient Welcome Page          ")
        print("-------------------------------------")
        op = input("Choose an Option:\n\n 1 = Register for Triage, 2 = Undergo Triage  ")

        if op == "1":
            self.set_strategy(RegisterForTriage())
        elif op == "2":
            self.set_strategy(UndergoTriage())
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
