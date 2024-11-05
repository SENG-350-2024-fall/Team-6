import pandas as pd
from abc import ABC, abstractmethod
import notification

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


class Nurse(User, notification.Observer):
    """Represents a Nurse."""
    def __init__(self, name, age, address, phone_number, username, password):
        super().__init__(name, age, address, phone_number, username, password)
        self.shift = None
        self.assigned_patients = []
        self.notifications = notification.Notification()
        self.notifications.add_observer(self)
        self.available = True
        self.can_conduct_triage = True
        self.shifts = []

    def get_role(self):
        return "Nurse"

    def update(self, message):
        print(f"New update for {self.username}")
        update_nurse_data(self)

    def view_assigned_patients(self):
        print("Assigned Patients:")
        if not self.assigned_patients:
            print("No patients assigned.")
        else:
            for patient in self.assigned_patients:
                print(f"- {patient}")

    @notification.notify_action("Patient {} has been assigned to you.")
    def add_patient(self, patient):
        self.assigned_patients.append(patient)

    @notification.notify_action("Patient {} has been removed from your care.")
    def remove_patient(self, patient):
        """Removes a discharged patient from the assigned list."""
        if patient in self.assigned_patients:
            self.assigned_patients.remove(patient)
        else:
            print(f"Patient {patient} is not in your assigned list.")

    def __str__(self):
        return f"Nurse: {self.username}"

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
                try:
                    # Exception detection on data integrity during user creation
                    user = user_factory.create_user(
                        row['Name'],
                        row['Age'],
                        row['Address'],
                        row['Phone'],
                        row['Username'],
                        row['Password']
                    )
                    users.append(user)
                except KeyError as e:
                    print(f"Missing field in {role}.csv: {e}")
                except ValueError as e:
                    print(f"Invalid data type in {role}.csv: {e}")
                except Exception as e:
                    print(f"Unexpected error while creating user: {e}")

            return users
        except FileNotFoundError:
            print(f"No user credentials file found for role: {role}.")
        except pd.errors.EmptyDataError:
            print(f"The file {filename} is empty.")
        except pd.errors.ParserError as e:
            print(f"Error parsing {filename}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while loading users: {e}")
        
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
