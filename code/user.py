import pandas as pd
from abc import ABC, abstractmethod
import notification

## All patients' list global variable
users_patients = []

# Abstract Base Class for User
class User(notification.Observer, ABC):
    def __init__(self, name, age, address, phone_number, username, password):
        self.name = name
        self.age = age
        self.address = address
        self.phone_number = phone_number
        self.username = username
        self.password = password
        self.notifications = notification.Notification()
        self.notifications.add_observer(self)

    @abstractmethod
    def get_role(self):
        pass
    def update(self, message):
        pass



# Concrete User Subclasses
class Doctor(User):
    def __init__(self, name, age, address, phone_number, username, password, specialization, available=True):
        super().__init__(name, age, address, phone_number, username, password)
        self.specialization = specialization
        self.available = available

    def get_role(self):
        return "Doctor"


class Patient(User):
    def __init__(self, name, age, address, phone_number, username, password):
        super().__init__(name, age, address, phone_number, username, password)
        self.status = "Waiting"

    def get_role(self):
        return "Patient"


class Nurse(User):
    """Represents a Nurse."""
    def __init__(self, name, age, address, phone_number, username, password, assigned_patients=None, available=True,
                 triage_ready=True, notifications=None, shift=""):
        super().__init__(name, age, address, phone_number, username, password)
        self.assigned_patients = assigned_patients if assigned_patients is not None else []
        self.available = available
        self.triage_ready = triage_ready
        self.shift = shift
        self.vitals_dict = {}

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
    def create_user(self, name, age, address, phone_number, username, password, specialization, available=True):
        return Doctor(name, age, address, phone_number, username, password, specialization, available)

class PatientFactory(UserFactory):
    def create_user(self, name, age, address, phone_number, username, password):
        return Patient(name, age, address, phone_number, username, password)


class NurseFactory(UserFactory):
    def create_user(self, name, age, address, phone_number, username, password, availability=True,
                    triage_ready=True, assigned_patients=None, notifications=None, shift="", vitals_dict=None):
        return Nurse(name, age, address, phone_number, username, password, assigned_patients,
                     availability, triage_ready, shift, vitals_dict)



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
    # @staticmethod
    def load_users(role):
        """Load users of a specific role from a CSV file and create instances of the corresponding class."""
        filename = f"{role}.csv"  # CSV file assumed to be named after the role (e.g., Doctor.csv, Patient.csv)
        users = []  # Reset or initialize an empty list for this call
        
        try:
            df = pd.read_csv(filename)
            
            # Check the role and adjust user creation logic as needed
            user_factory = UserLoader.role_factory_map.get(role.lower())
            if not user_factory:
                print(f"No factory defined for role: {role}.")
                return []

            for _, row in df.iterrows():
                try:
                    # Role-specific handling for attributes
                    if role.lower() == 'doctor':
                        user = user_factory.create_user(
                            row['Name'],
                            row['Age'],
                            row['Address'],
                            row['Phone'],
                            row['Username'],
                            row['Password'],
                            row['Specialization'],
                            row['Available']
                        )
                    elif role.lower() == 'patient':
                        user = user_factory.create_user(
                            row['Name'],
                            row['Age'],
                            row['Address'],
                            row['Phone'],
                            row['Username'],
                            row['Password']
                        )
                    elif role.lower() == 'nurse':
                        assigned_patients = row["AssignedPatients"].split(";") if pd.notna(row["AssignedPatients"]) else []
                        notifications = row["Notifications"].split(";") if pd.notna(row["Notifications"]) else []
                        
                        user = user_factory.create_user(
                            row['Name'],
                            row['Age'],
                            row['Address'],
                            row['Phone'],
                            row['Username'],
                            row['Password'],
                            availability=row['Availability'],
                            triage_ready=row['TriageReady'],
                            assigned_patients=assigned_patients,
                            shift=row['Shift']
                        )
                        
                        # Add notifications if available
                        for notification_msg in notifications:
                            user.notifications.add_notification(notification_msg)
                
                    elif role.lower() == 'system_administrator':
                        user = user_factory.create_user(
                            row['Name'],
                            row['Age'],
                            row['Address'],
                            row['Phone'],
                            row['Username'],
                            row['Password']
                        )
                    elif role.lower() == 'ed_staff':
                        user = user_factory.create_user(
                            row['Name'],
                            row['Age'],
                            row['Address'],
                            row['Phone'],
                            row['Username'],
                            row['Password']
                        )
                    else:
                        print(f"Role-specific logic not implemented for: {role}")
                        continue
                    
                    users.append(user)
                    
                except KeyError as e:
                    print(f"Missing field in {role}.csv: {e}")
                except ValueError as e:
                    print(f"Invalid data type in {role}.csv: {e}")
                except Exception as e:
                    print(f"Unexpected error while creating user: {e}")

            return users  # Return only users for the requested role
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
