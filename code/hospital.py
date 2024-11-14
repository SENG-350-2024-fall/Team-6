import csv
import os
from notification import Notification

# Creating hospital class using singleton pattern
class Hospital:
    instance = None
    csv_file_path = "hospital.csv"

    def __new__(cls, *args, **kwargs):
        # Implement Singleton pattern: only one instance can exist.
        if cls.instance is None:
            cls.instance = super(Hospital, cls).__new__(cls)
        return cls.instance

    def __init__(self, name="Default Hospital", edCapacity=100, location="Unknown"):
        # Initialize the Hospital instance with default or provided values.
        if not hasattr(self, '_initialized'):  # Prevent re-initialization
            self.name = name
            self.edCapacity = edCapacity
            self.currentEDLoad = 0  # Starting with zero patients in ED
            self.location = location
            self._initialized = True

            # Load hospital data from CSV or save the new instance to hospital.csv
            if os.path.exists(self.csv_file_path):
                self._load_from_csv()
            else:
                self._save_to_csv()

    def _save_to_csv(self):
        # Save the hospital's details to the hostpital.csv file if not existing in the file.
        with open(self.csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "location", "edCapacity", "currentEDLoad",])
            writer.writerow([self.name, self.location, self.edCapacity, self.currentEDLoad])

    def _load_from_csv(self):
        # Load the hospital's details from the CSV file.
        try:
            with open(self.csv_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.name = row["name"]
                    self.edCapacity = int(row["capacity"])
                    self.currentEDLoad = int(row["currentEDLoad"])
                    self.location = row["location"]
                    break
        except (FileNotFoundError, KeyError, ValueError) as e:
            print(f"Error loading hospital data")

    def updateEDCapacity(self, new_capacity):
        # Update the emergency department's maximum capacity and save to hospital.csv
        if new_capacity >= 0:
            self.edCapacity = new_capacity
            self._save_to_csv()
            print(f"Emergency department capacity updated to {new_capacity}.") #notification needs to get updated
            return True
        print("Invalid capacity update.")
        return False

    def incrementED(self):
        # Increment the current ED capacity by 1 if it's below maximum.
        if self.currentEDLoad < self.edCapacity:
            self.currentEDLoad += 1
            self._save_to_csv()
            print(f"Current ED capacity incremented to {self.currentEDLoad}.") #notification
            return True
        print("Emergency department is at full capacity.") #notification
        return False

    def decrementED(self):
        # Decrement the current ED capacity by 1 if it's above zero.
        if self.currentEDLoad > 0:
            self.currentEDLoad -= 1
            self._save_to_csv()
            print(f"Current ED capacity decremented to {self.currentEDCapacity}.") #notification
            return True
        print("Emergency department capacity is already at zero.")
        return False

    def getCurrentEDCapacity(self):
        # Return the current emergency department capacity.
        return self.currentEDLoad

    def setName(self, name):
        # Set the hospital's name and save to hospital.csv
        self.name = name
        self._save_to_csv()

    def getName(self):
        # Get the hospital's name
        return self.name

    def setLocation(self, location):
        # Set the hospital's location and save to hospital.csv
        self.location = location
        self._save_to_csv()

    def getLocation(self):
        # Get the hospital's location
        return self.location
