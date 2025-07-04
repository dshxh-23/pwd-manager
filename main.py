import sys, json, os
import pyperclip
from my_lib import getters, utilities


def main():
    user_name = get_name()

    utilities.print_ellipsis("searching the database", 2)

    if not user_exists(user_name):
        choice = getters.get_choice("y", "n", prompt="User does not exist. Do you want to register yourself?")
        if choice == "y":
            register_new_user(user_name)
            print("User successfully registered. You can login now")

    start_app(user_name)


# GET USER NAME
def get_name():
    return input("Name: ").strip().lower()  # Add error checking

# CHECK IF USER EXISTS
def user_exists(name):
    return True if os.path.exists(f"vaults/{name}.json") else False


# Set master password for new user
def set_master_password():
    while True:
        m_pwd = input("Enter Master Password: ")
        m_pwd2 = input("Re-enter Master Password: ")
        if m_pwd == m_pwd2:
            print("Master password set successfully!")
            return m_pwd
        else:
            print("Passwords do not match.. Try again.\n")


# === REGISTER NEW USER ===
def register_new_user(name):
    m_pwd = set_master_password()
    vault_data = make_vault(m_pwd, name)
    save_vault(vault_data, name)

# Make vault for new user
def make_vault(m_pwd, name):
    vault_data = {
        "master_password" : m_pwd,
        "data" : {},
    }
    return vault_data

# To save vault details in a json file
def save_vault(vault_data, name):
    with open(f"vaults/{name}.json", "w") as file:
        json.dump(vault_data, file, indent=4)


# === START APPLICATION ===
def start_app(user_name):

    tries = 3
    for i in range(tries):
        if validate_user(user_name, input("Password: ")):
            print(f"Welcome {user_name}! Successfully logged in!")
            break

        if not validate_user(user_name, input("Password: ")) and i<tries-1:
            print("Incorrect Password! Try again")
            continue
        
        sys.exit("Too many unsuccessful attempts...")

    
    while True:
        display_start_menu()
        choice = getters.get_int("Select Option: ", min_value=1, max_value=3)

        match choice:
            case 1: new_pwd(user_name)
            case 2: cpy_pwd(user_name)
            case 3:     
                utilities.print_ellipsis("Logging out", 3)
                sys.exit("Logged out successfully!")

# Validate user
def validate_user(name, pwd):
    vault_data = load_vault(name)
    return True if vault_data["master_password"] == pwd else False 
    
# Load vault
def load_vault(name):
    with open(f"vaults/{name}.json", "r") as file:
        vault_data = json.load(file)
    return vault_data

# Display menu
def display_start_menu():
    print("1.\tRecord new password")
    print("2.\tView existing password")
    print("3.\tLogout")

# Record new password
def new_pwd(user_name):
    acc_name = input("Website/App: ").lower()
    email = input("Email: ")
    user_id = input("User ID: ")
    while True:
        pwd = input("Password: ")
        pwd2 = input("Re-enter password: ")
        if pwd == pwd2:
            break
        else:
            print("Passwords do not match! Try again.")
    
    vault_data = load_vault(user_name)
    vault_data["data"][acc_name] = {
            "email" : email,
            "user_id" : user_id,
            "password" : pwd,
        }
    
    save_vault(vault_data, user_name)


# Copy existing password
def cpy_pwd(user_name):
    acc = input("Which account password do you want to copy?").lower()
    vault_data = load_vault(user_name)
    pyperclip.copy(vault_data['data'][acc]["password"])
    print("Password copied to clipboard successfully!")


if __name__ == "__main__":
    main()
