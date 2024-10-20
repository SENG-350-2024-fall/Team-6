import json
import os
import time

def load_credentials():
    try:
        with open("users.json") as f:
            data = json.load(f)
            return data["users"]
    except FileNotFoundError:
        print("No user credentials file found.")
        return []

def check_credentials(username, password):
    users = load_credentials()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user 
    return None

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user = check_credentials(username, password)
    if user:
        clear_terminal()
        time.sleep(1)
        print(f"Welcome, {user['name']}!")
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