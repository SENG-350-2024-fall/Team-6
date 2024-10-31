import pandas as pd
import os
import time

def load_credentials(role):
    filename = f"{role}.csv"  # Assuming CSV files are named after the role
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(filename)
        return df  # Return the DataFrame containing user data
    except FileNotFoundError:
        print(f"No user credentials file found for role: {role}.")
        return pd.DataFrame()  # Return an empty DataFrame

def check_credentials(role, username, password):
    users = load_credentials(role)
    # Check if the username and password exist in the DataFram
    user = users[(users["Username"] == username) & (users["Password"] == password)]
    if not user.empty:
        return user.iloc[0]['Name']
    return None

def login(role):
    username = input("Enter your username: ")
    password = input("Enter your password: ")


    user = check_credentials(role, username, password)
    if user:
        clear_terminal()
        time.sleep(1)
        print(f"Welcome, {user}!")
        return user  # Return the user object for further use
    else:
        clear_terminal()
        time.sleep(1)
        print("Invalid username or password.")
        time.sleep(1)
        return None

def clear_terminal():
    # Clear the terminal screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

# Example usage:
# role = input("Enter your role (admin, doctor, nurse, etc.): ")
# logged_in_user = login(role)
