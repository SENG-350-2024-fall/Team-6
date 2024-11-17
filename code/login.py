import os
import time
from data_stores import all_users  # Import all_users from data_stores
import getpass

login_check = 0

def load_credentials(role):
    """
    Fetch users of a specific role from all_users.
    Returns a list of user dictionaries for the specified role.
    """
    return all_users.get(role, [])

def check_credentials(role, username, password):
    """
    Check if the username and password match for the given role in all_users.
    """
    users = load_credentials(role)
    # Find the user with matching username and password
    for user in users:
        if user.username == username and user.password == password:
            return user
    return None

def login(role):
    """
    Prompt for login credentials and verify against all_users data.
    """
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")


    user = check_credentials(role, username, password)
    if user is not None:
        clear_terminal()
        time.sleep(1)
        print(f"Welcome, {user.name}!")
        set_invalid_login(0)
        return user  # Return the user name for further use
    else:
        clear_terminal()
        time.sleep(1)
        print("Invalid username or password.")
        set_invalid_login(1)
        time.sleep(1)
        return None
    
def set_invalid_login(val):
    global login_check
    login_check = val

def get_invalid_login():
    return login_check

def clear_terminal():
    """
    Clear the terminal screen based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# Example usage:
# role = input("Enter your role (admin, doctor, nurse, etc.): ")
# logged_in_user = login(role)
