# 🔐 Password Manager (Python CLI)

A command-line password manager that allows you to securely store, retrieve, and manage your account credentials locally. User authentication is enforced using a master password. Passwords are copied to your clipboard for convenience.

---

## 🚀 Features

- Create a new user profile with a master password
- Log in with master password authentication
- Store password entries with:
    * Account name (e.g., "github.com")
    * Email (optional)
    * User ID (optional)
    * Password (mandatory)
- Copy passwords to clipboard using the `pyperclip` module
- Edit existing account details (email, user ID, password)
- Data is stored locally in a per-user JSON file in the `vaults/` directory
- Simple, user-friendly CLI with clear menus and separators

---

## 🛠️ How to Use

1. **Start the Program**
   - Run `python main.py` in your terminal.

2. **User Identification**
   - Enter your name when prompted.
   - If you are a new user, you will be guided to create a master password.
   - If you are an existing user, you will be prompted to log in with your master password.

3. **Main Menu Options**
   - After login, you can:
     1. **Record new account details**: Add a new account with its password, email, and user ID.
     2. **View existing account details**: Retrieve and copy a password for a saved account to your clipboard.
     3. **Modify existing account details**: Update the email, user ID, or password for any saved account.
     4. **Logout**: Securely log out of the application.

4. **Password Management**
   - When adding or modifying a password, you must enter the password securely (input is hidden).
   - All account data is saved in your personal JSON file inside `vaults/`.

5. **Clipboard Integration**
   - When viewing a password, it is automatically copied to your clipboard using the `pyperclip` module.

---

## 💾 Data Storage

All user data is stored in the `vaults/` directory.

* Each user has a separate file named `.username.json` (the username is lowercased and stripped of spaces).
* Example structure of the JSON:

```json
{
  "user_name": "dhyey",
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

## 💡 Planned Enhancements

- **Command-line shortcuts**
  - Quick password retrieval using command-line arguments (e.g., `python main.py --name dhyey --pwd 1234 --acc github.com`)
- **Password Encryption**
  - Encrypt all stored passwords using the `cryptography` library (e.g., `Fernet`, PBKDF2 with salt)
- **Unit Tests**
  - Add test coverage for core features using `pytest`
- **Random Password Generator**
  - Add a tool to generate secure random passwords for new accounts
- **Improved CLI UI**
  - Use libraries like `tabulate` or `rich` for better table formatting and colored output

---

## 🤝 Contributions

Suggestions and contributions are welcome! Feel free to fork the repo and submit a pull request to add or improve features.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
