import sys
import json
import os
import pyperclip
from my_py_lib import getters, printers, setters, utilities



### =============== CONSTANTS =============== ###
BANNER = """
=====================================
   🔐 Welcome to Password Manager!   
=====================================
"""
SEPARATOR = "-----------------------------------"
VAULT_DIR = "vaults"
PWD_ATTEMPTS = 2



### =============== PASSWORD VAULT =============== ###
class PasswordVault:

    # Constructor
    def __init__(self, name):
        """
        Initialize the PasswordVault. If the vault exists, load and decrypt it.
        If not, create a new vault with the provided master password.
        Raises ValueError if master_password is not provided when required.
        """

        """
        ALL VAULT FUNCTIONALITIES:
        """
        self.name = name.lower().strip()
        self.file_path = os.path.join(VAULT_DIR, f".{self.name}.json")

        # Log-in if user account already exists
        if os.path.exists(self.file_path):
            choice = getters.get_choice("y", "n", prompt="An account already exists.. Do you want to log-in?")
            
            # Exit if user does not want to do anything
            if not choice == 'y':
                sys.exit("See you soon...")
                
            # Load vault data    
            self.vault_data = self._load_vault()

            # Authenticate user
            if not self._authenticate_user():
                sys.exit("User authentication failed..")

        else:
            print("Account does not exist. Creating a new account")
            self._create_vault()


    ## ------------ VAULT OPERATIONS ------------ ##
    # Save vault in a json file
    def _save_vault(self, vault_data):
        with open(self.file_path, "w") as file:
            json.dump(vault_data, file, indent=4)
        self.vault_data = vault_data
    
    # Create new empty vault
    def _create_vault(self):
        m_pwd = setters.set_pwd()
        vault_data = {
            "user_name" : self.name,
            "master_password" : m_pwd,
            "data" : {},
        }
        self._save_vault(vault_data)

    # To initially load vault data into self.vault_data variable
    def _load_vault(self):
        with open(self.file_path, "r") as file:
            vault_data = json.load(file)
        return vault_data
    
    # Append new data to vault
    def _add_acc_to_vault(self, acc_name, acc_data):
        """ pass acc name as a string and acc details as a dict """
        vault_data = self._load_vault()
        vault_data["data"][acc_name] = acc_data
        self._save_vault(vault_data)

    def _authenticate_user(self):
        m_pwd = self.vault_data["master_password"]
        if not utilities.chk_pwd(m_pwd, attempts=PWD_ATTEMPTS):
            return False
        else:
            print("Successfully logged-in")
            return True
        
    
    ## ------------ USER OPERATIONS ------------ ##
    # Select what user want's to do
    def get_operation(self):
        print(SEPARATOR)
        print("\nWhat would you like to do?")
        print("1.\tRecord new account details")
        print("2.\tView existing account details")
        print("3.\tModify existing account details")
        print("4.\tLogout")
        print(SEPARATOR)
        return getters.get_int(min_value=1, max_value=4)

    # Record a new account to vault
    def record_acc(self):
        print(SEPARATOR)
        print("\nEnter new account details:")
        acc_name = input("Account Name: ")
        acc_email = input("Account Email: ")
        acc_id = input("User ID: ")
        acc_pwd = getters.get_pwd("Account Password: ")
        acc_data = {
            "email" : acc_email,
            "user_id" : acc_id,
            "password" : acc_pwd,
        }
        self._add_acc_to_vault(acc_name, acc_data)
        printers.print_ellipsis("Saving", n=3, delay=0.3)
        print("Account added successfully!\n")
        print(SEPARATOR)

    # Retrieve acc details and copy password
    def retrieve_acc(self, acc_name):
        print(SEPARATOR)
        if acc_name not in list(self.vault_data['data'].keys()):
            print("No such account in the vault. Kindly add account first.\n")
            print(SEPARATOR)
            return
        print(f"Account Name: {acc_name}")
        print(f"Registered Email: {self.vault_data['data'][acc_name]['email']}")
        print(f"User ID: {self.vault_data['data'][acc_name]['user_id']}")
        pyperclip.copy(self.vault_data['data'][acc_name]['password'])
        print("Password copied to clipboard!\n")
        print(SEPARATOR)

    # Modify a particular account details
    def modify_acc(self, acc_name):
        print(SEPARATOR)
        if acc_name not in self.vault_data['data']:
            print("No such account in the vault. Kindly add account first.\n")
            print(SEPARATOR)
            return

        acc_data = self.vault_data['data'][acc_name]
        print(f"Current details for '{acc_name}':")
        print(f"  Email: {acc_data['email']}")
        print(f"  User ID: {acc_data['user_id']}")
        print("Leave a field blank to keep it unchanged.\n")

        new_email = input("New Email: ").strip()
        new_user_id = input("New User ID: ").strip()
        change_pwd = getters.get_choice("y", "n", prompt="Change password?")

        if new_email:
            acc_data['email'] = new_email
        if new_user_id:
            acc_data['user_id'] = new_user_id
        if change_pwd == "y":
            acc_data['password'] = getters.get_pwd("New Password: ")

        self._add_acc_to_vault(acc_name, acc_data)
        printers.print_ellipsis("Updating", n=3, delay=0.3)
        print("Account details updated successfully!\n")
        print(SEPARATOR)


### =============== CORE PROGRAM FLOW =============== ###
def main():
    os.makedirs(VAULT_DIR, exist_ok=True)
    print(BANNER)

    user_name = input("What's your first name? ")   # get user name
    vault = PasswordVault(user_name)                # initialize vault

    mainloop(vault)


def mainloop(vault):
    while True:
        choice = vault.get_operation()
        match choice:
            case 1: vault.record_acc()
            case 2: 
                acc_name = input(f"Which acc details do you want? {list(vault.vault_data['data'].keys())}: ")
                vault.retrieve_acc(acc_name)
            case 3:
                acc_name = input(f"Which acc details do you want to modify? {list(vault.vault_data['data'].keys())}")
                vault.modify_acc(acc_name)
            case 4: 
                printers.print_ellipsis("Logging out", n=4, delay=0.5)
                return



### =============== CALL MAIN =============== ###
if __name__ == "__main__":
    main()