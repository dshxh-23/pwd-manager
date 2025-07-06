import sys
import json
import os
import pyperclip
from my_py_lib import getters, utilities

# === CLI Decorations ===
BANNER = """
=====================================
   🔐 Welcome to Password Manager!   
=====================================
"""
SEPARATOR = "-------------------------------------"


def main():
    print(BANNER)
    user_name = get_name()

    utilities.print_ellipsis("Searching the database", 2)

    if not user_exists(user_name):
        choice = getters.get_choice("y", "n", prompt=f"User '{user_name}' does not exist. Do you want to register?")
        if choice == "y":
            register_new_user(user_name)
            print("\nUser successfully registered. Please log in to continue.\n")
            print(SEPARATOR)
            user_name = get_name()  # Ask for username again before login
        else:
            print("Exiting...")
            sys.exit(0)

    start_app(user_name)


def get_name():
    while True:
        name = input("\nEnter your name: ").strip().lower()
        if name:
            return name
        print("Name cannot be empty. Please try again.")


def user_exists(name):
    return os.path.exists(f"vaults/{name}.json")


def set_master_password():
    while True:
        m_pwd = input("\nSet Master Password: ")
        m_pwd2 = input("Re-enter Master Password: ")
        if m_pwd == m_pwd2 and m_pwd:
            print("\033[92mMaster password set successfully!\033[0m\n")
            return m_pwd
        else:
            print("\033[91mPasswords do not match or empty. Try again.\033[0m\n")


def register_new_user(name):
    os.makedirs("vaults", exist_ok=True)
    m_pwd = set_master_password()
    vault_data = make_vault(m_pwd)
    save_vault(vault_data, name)


def make_vault(m_pwd):
    return {
        "master_password": m_pwd,
        "data": {},
    }


def save_vault(vault_data, name):
    os.makedirs("vaults", exist_ok=True)
    with open(f"vaults/{name}.json", "w") as file:
        json.dump(vault_data, file, indent=4)


def start_app(user_name):
    tries = 3
    for i in range(tries):
        print(f"\n{SEPARATOR}")
        pwd = input(f"Enter master password for '{user_name}': ")
        if validate_user(user_name, pwd):
            print(f"\033[92mWelcome {user_name}! Successfully logged in!\033[0m\n")
            break
        else:
            if i < tries - 1:
                print("\033[91mIncorrect Password! Try again.\033[0m")
            else:
                sys.exit("\033[91mToo many unsuccessful attempts...\033[0m")

    while True:
        display_start_menu()
        choice = getters.get_int("Select Option: ", min_value=1, max_value=3)
        match choice:
            case 1:
                new_pwd(user_name)
            case 2:
                cpy_pwd(user_name)
            case 3:
                utilities.print_ellipsis("Logging out", 3)
                print("\033[94mLogged out successfully!\033[0m")
                sys.exit(0)


def validate_user(name, pwd):
    vault_data = load_vault(name)
    return vault_data["master_password"] == pwd


def load_vault(name):
    with open(f"vaults/{name}.json", "r") as file:
        return json.load(file)


def display_start_menu():
    print(f"\n{SEPARATOR}")
    print("1.\tRecord new password")
    print("2.\tView existing password")
    print("3.\tLogout")
    print(SEPARATOR)


def new_pwd(user_name):
    acc_name = input("Website/App: ").strip().lower()
    email = input("Email: ").strip()
    user_id = input("User ID: ").strip()
    while True:
        pwd = input("Password: ")
        pwd2 = input("Re-enter password: ")
        if pwd == pwd2 and pwd:
            break
        else:
            print("\033[91mPasswords do not match or empty! Try again.\033[0m")

    vault_data = load_vault(user_name)
    vault_data["data"][acc_name] = {
        "email": email,
        "user_id": user_id,
        "password": pwd,
    }
    save_vault(vault_data, user_name)
    print("\033[92mPassword saved successfully!\033[0m")


def cpy_pwd(user_name):
    acc = input("Which account password do you want to copy? ").strip().lower()
    vault_data = load_vault(user_name)
    if acc in vault_data['data']:
        pyperclip.copy(vault_data['data'][acc]["password"])
        print("\033[92mPassword copied to clipboard successfully!\033[0m")
    else:
        print("\033[91mAccount not found!\033[0m")


if __name__ == "__main__":
    main()
