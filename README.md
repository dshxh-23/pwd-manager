# 🔐 Password Manager (Python CLI)

A command-line password manager that allows users to store, retrieve, and manage their account credentials locally. User authentication is supported using a master password.

---

## 📦 Features (Implemented in Version 1)

- Create a new user profile with a master password
- Log in with master password authentication
- Store password entries with:
    * Account name (e.g., "github.com")
    * Email (optional)
    * User ID (optional)
    * Password (mandatory)
- Copy passwords to clipboard using the `pyperclip` module
- Data is stored locally in a per-user JSON file

---

## 🚦 How the Program Works

1. **Start the Program**
   - Run `python main.py` in your terminal.

2. **User Identification**
   - The program prompts you to enter your name.
   - If you are a new user, you will be asked if you want to register.

3. **Registering a New User**
   - If you choose to register, you must set a master password (entered twice for confirmation).
   - A new vault file is created for you in the `vaults/` directory, storing your master password and an empty data section.

4. **Logging In**
   - Existing users are prompted to enter their master password (up to 3 attempts).
   - On successful login, you access your personal vault.

5. **Main Menu Options**
   - After login, you can:
     1. **Record new password**: Add a new account with its password, email, and user ID.
     2. **View existing password**: Retrieve and copy a password for a saved account to your clipboard.
     3. **Logout**: Securely log out of the application.

6. **Password Management**
   - When adding a new password, you must confirm the password by entering it twice.
   - All account data is saved in your personal JSON file inside `vaults/`.

7. **Clipboard Integration**
   - When viewing a password, it is automatically copied to your clipboard using the `pyperclip` module.

---

## 💾 Where Is Data Stored?

All user data is stored in the `vaults/` directory.

* Each user has a separate file named `<username>.json`
* Example structure of the JSON:

  ```json
  {
    "master_password": "1234",
    "data": {
      "github.com": {
        "email": "me@example.com",
        "user_id": "dshxh-23",
        "password": "my_password"
      }
    }
  }
  ```

---

## 💠 Planned Enhancements

Here are some features planned for future versions:

1. **Command-line shortcuts**

   * Quick password retrieval using:

     ```bash
     python main.py --name dhyey --pwd 1234 --acc github.com
     ```

2. **Edit existing password records**

   * Modify email, user ID, or password for any saved account.

3. **Password Encryption**

   * Encrypt all stored passwords using the `cryptography` library (e.g., `Fernet`, PBKDF2 with salt).

4. **Unit Tests**

   * Add test coverage for core features using or `pytest`.

5. **Random Password Generator**

   * Add a tool to generate secure random passwords for new accounts.

---

## 🤝 Contributions

Suggestions and contributions are welcome! Feel free to fork the repo and submit a pull request once features are added or improved.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---
