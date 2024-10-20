import pandas as pd
import numpy as np
from csv import writer
from datetime import date
import os


class patient:

    status = "Triage is Not Taken"
    triageStatus = "Idle"

    def __init__(self, username: str, password: str):
        pass

    def login(self):

        print()
        print("    Patient Login Page      ")
        print("----------------------------")

        username = input("Username: ")
        password = input("Password: ")

        try:
            data = pd.read_csv("patients_credentials.csv")
        except:
            print("Patient Credential File is Not Found!!")
            return
        
        check = 0

        for un, pas in list(data[["username", "password"]].values):
            if str.lower(username) == str.lower(un) and str.lower(pas) == str.lower(
                password
            ):

                check = 1
                break

        if check == 1:

            print("You have logged in successfully!")

        else:

            x = input("Please re-enter credentials or input 1 register! ")
            if x == str(1):
                patient_register()
            else:
                patient_login()
                check = 0

    def register(self):

        print()
        print("    Patient Registering Page      ")
        print("-----------------------------------")

        username = input("Username: ")
        password = input("Password: ")
        address = input("Address: ")
        phoneNumber = input("Phone Number: ")
        
        try:
            data = pd.read_csv("patients_credentials.csv")
        except:
            print("Patient Credential File is Not Found!!")
            return

        for un, pas in list(data[["username", "password"]].values):

            if str.lower(username) == str.lower(un) and str.lower(pas) == str.lower(
                password
            ):
                return "You are already registered!"

        with open("patients_credentials.csv", "a", newline="") as csv_file:
            writer_obj = writer(csv_file)
            writer_obj.writerow([username, password, address, phoneNumber])
            print("You have been registered successfully!")
            csv_file.close()

            return 1

    def undergoTriage(self):

        print()
        print("    Virtual Triage Page   ")
        print("-------------------------------------")

        username = input("Username: ")
        full_name = input("Full Name: ")

        q1 = input("What are your symptomps?  ")
        q2 = input("How long you have been experiencing them?  ")
        q3 = input("Have you experienced this symptom before?  ")
        q4 = input("Has this issue affected your daily activities or work?  ")

        answers = [q1 + "   ", q2 + "   ", q3 + "   ", q4 + "   "]
        
        try:
            data = pd.read_csv("triage.csv")
        except:
            print("Triag File is Not Found!!")
            return
        
        registered = 0
        
        for i in range(len(data)):

            if (
                data["username"].iloc[i] == username
                and data["full_name"].iloc[i] == full_name
            ):
                data["answers"].iloc[i] = answers
                status = "Triage is taken."
                data.to_csv("triage.csv", sep=",", index=False, encoding="utf-8")
                print("Answers Are Saved Successfully!")
                registered = 1
                break
        if(registered == 0):
            print("Please Register for the Triage First!")
            
        return status

    def registerForTriage(self):

        print()
        print("    Virtual Triage Registration   ")
        print("-------------------------------------")

        username = input("Username: ")
        full_name = input("Full Name: ")
        age = input("Age: ")
        reason = input("Reason: ")
        diagnosed_diseases = input("Diagnosed Diseases: ")
        today = date.today()

        with open("triage.csv", "a", newline="") as csv_file:
            writer_obj = writer(csv_file)
            writer_obj.writerow(
                [username, full_name, age, reason, diagnosed_diseases, today, "NA"]
            )
            print("Your Request Have Been Submitted!")
            csv_file.close()
            triageStatus = "Registeration Confirmed"

        return triageStatus
