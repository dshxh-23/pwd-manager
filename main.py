import sys
import json
import os
import argparse
import pyperclip
from my_py_lib import getters, utilities

# CRYPTOGRAPHIC FUNCTIONS AND ENCRYPTED VAULT HANDLING (moved below dependencies)
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import secrets

# === CLI Decorations ===
BANNER = """
=====================================
   🔐 Welcome to Password Manager!   
=====================================
"""
SEPARATOR = "-------------------------------------"


def main():
    """Entry point for the Password Manager CLI app."""
    print(BANNER)
    args = parse_args()

    # Quick retrieval mode via CLI arguments
    if args.name and args.pwd and args.acc:
        quick_retrieve(args)
        return

    # Interactive mode
    user_name = get_name()
    utilities.print_ellipsis("Searching the database", 2)

    if not user_exists(user_name):
        # Offer registration if user does not exist
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


def parse_args():
    """Parse command-line arguments for quick retrieval."""
    parser = argparse.ArgumentParser(description="Store all your passwords securely")
    parser.add_argument("--name", help="Name of the user", default="")
    parser.add_argument("--pwd", help="Master password", default="")
    parser.add_argument("--acc", help="Account name", default="")
    return parser.parse_args()


def quick_retrieve(args):
    """Quickly retrieve and copy a password using CLI arguments."""
    if not user_exists(args.name):
        sys.exit("User does not exist")
    if not validate_user(args.name, args.pwd):
        sys.exit("Incorrect password")
    vault_data = load_vault(args.name)
    if args.acc in vault_data['data']:
        pyperclip.copy(vault_data['data'][args.acc]["password"])
        sys.exit("\033[92mPassword copied to clipboard successfully!\033[0m")
    else:
        sys.exit("\033[91mAccount not found!\033[0m")


def get_name():
    """Prompt the user for their name (non-empty, lowercase)."""
    while True:
        name = input("\nEnter your name: ").strip().lower()
        if name:
            return name
        print("Name cannot be empty. Please try again.")


def user_exists(name):
    """Check if a user vault file exists."""
    return os.path.exists(f"vaults/{name}.json")


def set_master_password():
    """Prompt user to set and confirm a master password using getters.get_pwd."""
    m_pwd = getters.get_pwd("Set Master Password: ")
    print("\033[92mMaster password set successfully!\033[0m\n")
    return m_pwd


def make_vault(m_pwd):
    """Create a new vault data structure."""
    return {
        "master_password": m_pwd,
        "data": {},
    }


def register_new_user(name):
    """Register a new user and create their encrypted vault file."""
    os.makedirs("vaults", exist_ok=True)
    m_pwd = set_master_password()
    salt = generate_salt()
    key = derive_key(m_pwd, salt)
    vault_data = make_vault(m_pwd)
    encrypted_vault = encrypt_data(vault_data, key)
    save_encrypted_vault(encrypted_vault, salt, name)


def start_app(user_name):
    """Authenticate user and present the main menu loop."""
    tries = 3
    for i in range(tries):
        print(f"\n{SEPARATOR}")
        pwd = getters.get_pwd(f"Enter master password for '{user_name}': ")
        with open(f"vaults/{user_name}.json", "rb") as file:
            salt = file.readline().strip()
            encrypted = file.read()
        key = derive_key(pwd, salt)
        try:
            vault_data = decrypt_data(encrypted, key)
            print(f"\033[92mWelcome {user_name}! Successfully logged in!\033[0m\n")
            break
        except Exception:
            if i < tries - 1:
                print("\033[91mIncorrect Password! Try again.\033[0m")
            else:
                sys.exit("\033[91mToo many unsuccessful attempts...\033[0m")
    else:
        sys.exit("\033[91mFailed to login.\033[0m")

    while True:
        display_start_menu()
        choice = getters.get_int("Select Option: ", min_value=1, max_value=3)
        match choice:
            case 1:
                new_pwd(user_name, vault_data, key)
            case 2:
                cpy_pwd(user_name, vault_data)
            case 3:
                utilities.print_ellipsis("Logging out", 3)
                print("\033[94mLogged out successfully!\033[0m")
                sys.exit(0)


def display_start_menu():
    """Display the main menu options."""
    print(f"\n{SEPARATOR}")
    print("1.\tRecord new password")
    print("2.\tView existing password")
    print("3.\tLogout")
    print(SEPARATOR)


def new_pwd(user_name, vault_data, key):
    """Add a new password entry to the user's vault."""
    acc_name = input("Website/App: ").strip().lower()
    email = input("Email: ").strip()
    user_id = input("User ID: ").strip()
    pwd = getters.get_pwd("Password: ")
    vault_data["data"][acc_name] = {
        "email": email,
        "user_id": user_id,
        "password": pwd,
    }
    save_vault(vault_data, user_name, key)
    print("\033[92mPassword saved successfully!\033[0m")


def cpy_pwd(user_name, vault_data):
    """Copy an existing password to the clipboard."""
    acc = input("Which account password do you want to copy? ").strip().lower()
    if acc in vault_data['data']:
        pyperclip.copy(vault_data['data'][acc]["password"])
        print("\033[92mPassword copied to clipboard successfully!\033[0m")
    else:
        print("\033[91mAccount not found!\033[0m")


# CRYPTOGRAPHIC FUNCTIONS AND ENCRYPTED VAULT HANDLING (moved below dependencies)
def generate_salt(length=16):
    """Generate a cryptographically secure random salt."""
    return secrets.token_bytes(length)


def derive_key(password, salt, iterations=390000):
    """Derive a key from the password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_data(data, key):
    """Encrypt data (dict) using the provided key."""
    f = Fernet(key)
    json_data = json.dumps(data).encode()
    return f.encrypt(json_data)


def decrypt_data(token, key):
    """Decrypt data using the provided key."""
    f = Fernet(key)
    decrypted = f.decrypt(token)
    return json.loads(decrypted.decode())


def save_encrypted_vault(encrypted_vault, salt, name):
    """Save the encrypted vault and salt to a JSON file."""
    os.makedirs("vaults", exist_ok=True)
    with open(f"vaults/{name}.json", "wb") as file:
        # Store salt and encrypted vault as binary
        file.write(salt + b"\n" + encrypted_vault)


def save_vault(vault_data, name, key):
    """Encrypt and save the vault data to a JSON file using the provided key."""
    with open(f"vaults/{name}.json", "rb") as file:
        salt = file.readline().strip()
    encrypted_vault = encrypt_data(vault_data, key)
    save_encrypted_vault(encrypted_vault, salt, name)


def load_vault(name):
    """Load and decrypt a user's vault data from file."""
    with open(f"vaults/{name}.json", "rb") as file:
        salt = file.readline().strip()
        encrypted = file.read()
    for _ in range(3):
        pwd = getters.get_pwd("Enter master password: ")
        key = derive_key(pwd, salt)
        try:
            return decrypt_data(encrypted, key)
        except Exception:
            print("\033[91mIncorrect password or corrupted vault!\033[0m")
    sys.exit("\033[91mFailed to load vault: incorrect password.\033[0m")


def validate_user(name, pwd):
    """Check if the provided password matches the user's master password by attempting decryption."""
    with open(f"vaults/{name}.json", "rb") as file:
        salt = file.readline().strip()
        encrypted = file.read()
    key = derive_key(pwd, salt)
    try:
        vault_data = decrypt_data(encrypted, key)
        return vault_data["master_password"] == pwd
    except Exception:
        return False


if __name__ == "__main__":
    main()