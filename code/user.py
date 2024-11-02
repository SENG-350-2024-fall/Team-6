import pandas as pd
from abc import ABC, abstractmethod

# Abstract Base Class for User
class User(ABC):
    def __init__(self, name, age, address, phone_number, username, password):
        self.name = name
        self.age = age
        self.address = address
        self.phone_number = phone_number
        self.username = username
        self.password = password

    @abstractmethod
    def get_role(self):
        pass


# Concrete User Subclasses
class Doctor(User):
    def __init__(self, name, age, address, phone_number, username, password):
        super().__init__(name, age, address, phone_number, username, password)
        self.available = True

    def get_role(self):
        return "Doctor"


class Patient(User):
    def __init__(self, name, age, address, phone_number, username, password):
        super().__init__(name, age, address, phone_number, username, password)
        self.status = "Waiting"

    def get_role(self):
        return "Patient"


class Nurse(User):
    def __init__(self, name, age, address, phone_number, username, password):
        super().__init__(name, age, address, phone_number, username, password)
        self.shift = None

    def get_role(self):
        return "Nurse"


class SystemAdmin(User):
    def __init__(self, name, age, address, phone_number, username, password):
        super().__init__(name, age, address, phone_number, username, password)
        self.admin_level = "High"

    def get_role(self):
        return "SystemAdmin"


class EdStaff(User):
    def __init__(self, name, age, address, phone_number, username, password):
        super().__init__(name, age, address, phone_number, username, password)

    def get_role(self):
        return "EdStaff"


# Abstract Factory
class UserFactory(ABC):
    @abstractmethod
    def create_user(self, name, age, address, phone_number, username, password):
        pass

# Concrete Factories for each User role
class DoctorFactory(UserFactory):
    def create_user(self, name, age, address, phone_number, username, password):
        return Doctor(name, age, address, phone_number, username, password)


class PatientFactory(UserFactory):
    def create_user(self, name, age, address, phone_number, username, password):
        return Patient(name, age, address, phone_number, username, password)


class NurseFactory(UserFactory):
    def create_user(self, name, age, address, phone_number, username, password):
        return Nurse(name, age, address, phone_number, username, password)


class SystemAdminFactory(UserFactory):
    def create_user(self, name, age, address, phone_number, username, password):
        return SystemAdmin(name, age, address, phone_number, username, password)


class EdStaffFactory(UserFactory):
    def create_user(self, name, age, address, phone_number, username, password):
        return EdStaff(name, age, address, phone_number, username, password)


# Factory Loader to load users from CSV
class UserLoader:
    role_factory_map = {
        'doctor': DoctorFactory(),
        'patient': PatientFactory(),
        'nurse': NurseFactory(),
        'system_administrator': SystemAdminFactory(),
        'ed_staff': EdStaffFactory()
    }

    @staticmethod
    def load_users(role):
        """Load users of a specific role from a CSV file and create instances of the corresponding class."""
        filename = f"{role}.csv"  # CSV file assumed to be named after the role (e.g., Doctor.csv, Patient.csv)
        try:
            df = pd.read_csv(filename)
            users = []
            
            # Get the factory for the role
            user_factory = UserLoader.role_factory_map.get(role.lower())
            if not user_factory:
                print(f"No factory defined for role: {role}.")
                return []

            # Use the factory to create instances of the class for each row in the DataFrame
            for _, row in df.iterrows():
                user = user_factory.create_user(
                    row['Name'],
                    row['Age'],
                    row['Address'],
                    row['Phone'],
                    row['Username'],
                    row['Password']
                )
                users.append(user)

            return users
        except FileNotFoundError:
            print(f"No user credentials file found for role: {role}.")
            return []
    
    @staticmethod
    def load_all_users():
        """Load users for all roles and return them as a dictionary with roles as keys."""
        roles = UserLoader.role_factory_map.keys()
        all_users = {}
        
        for role in roles:
            users = UserLoader.load_users(role)
            if users:
                all_users[role] = users
            else:
                print(f"No users found for role: {role}.")
                
        return all_users
