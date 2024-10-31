# user.py
import pandas as pd

class User:
    def __init__(self, name, age, address, phone_number, username, password):
        self.name = name
        self.age = age
        self.address = address
        self.phone_number = phone_number
        self.username = username
        self.password = password

class Doctor(User):
    def __init__(self, name, age, address, phone_number, username, password):
        super().__init__(name, age, address, phone_number, username, password)
        self.available = True

class Patient(User):
    def __init__(self, name, age, address, phone_number, username, password):
        super().__init__(name, age, address, phone_number, username, password)
        self.status = "Waiting"

class Nurse(User):
    def __init__(self, name, age, address, phone_number, username, password):
        super().__init__(name, age, address, phone_number, username, password)
        self.shift = None

class SystemAdmin(User):
    def __init__(self, name, age, address, phone_number, username, password):
        super().__init__(name, age, address, phone_number, username, password)
        self.admin_level = "High"

class EdStaff(User):
    def __init__(self, name, age, address, phone_number, username, password):
        super().__init__(name, age, address, phone_number, username, password)
    
class UserFactory:
    @staticmethod
    def load_users(role):
        """Load users of a specific role from a CSV file and create instances of the corresponding class."""
        filename = f"{role}.csv"  # CSV file assumed to be named after the role (e.g., Doctor.csv, Patient.csv)
        try:
            df = pd.read_csv(filename)
            users = []
            
            # Map roles to classes
            role_class_map = {
                'doctor': Doctor,
                'patient': Patient,
                'nurse': Nurse,
                'system_administrator': SystemAdmin,
                'ed_staff': EdStaff
            }

            # Get the class based on role, default to None if the role is not found
            user_class = role_class_map.get(role.lower())
            if not user_class:
                print(f"No class defined for role: {role}.")
                return []

            # Create instances of the class for each row in the DataFrame
            for _, row in df.iterrows():
                user = user_class(
                    row['name'],
                    row['age'],
                    row['address'],
                    row['phone_number'],
                    row['username'],
                    row['password']
                )
                users.append(user)

            return users
        except FileNotFoundError:
            print(f"No user credentials file found for role: {role}.")
            return []