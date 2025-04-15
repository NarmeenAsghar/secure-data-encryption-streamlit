
# 🔐 **Secure Data Encryption Vault** 🗝️

Welcome to the **Secure Data Encryption Vault**! This app allows you to encrypt, store, and securely retrieve confidential data using a passkey. Access is restricted after multiple failed attempts to ensure privacy and security.

## 🌟 **Features**

- 🔒 **Encrypt & Store Data**: Securely encrypt your data using a passkey and store it.
- 🔓 **Retrieve Data**: Retrieve and decrypt your stored data with the correct passkey and identifier.
- 🚫 **Lock Access**: After multiple failed attempts, access to the data will be locked.
- 🔑 **Admin Reauthorization**: Admin can reauthorize access with a master password.

## 🛠️ **Requirements**

To run this app, make sure you have the following installed:

- Python 3.x
- Streamlit
- Cryptography

## 📝 **Features & Pages**

### 1️⃣ **Home Page** 🏠
- Get an overview of the app's capabilities:
  - 🔐 **Encrypt and Store Confidential Data**
  - 🔓 **Retrieve it using a Passkey**
  - 🚫 **Lock Access after Multiple Failed Attempts**

### 2️⃣ **Store Data Page** 📂
- **Encrypt and Store**: Users can input a unique identifier, passkey, and text data.
  - The data is encrypted and stored securely with the hashed passkey.

### 3️⃣ **Retrieve Data Page** 🔍
- **Retrieve Data**: Users enter their identifier and passkey to decrypt and view their stored data.
  - If the wrong passkey is entered 3 times, the user’s access will be locked.

### 4️⃣ **Login Page** 🔑
- **Reauthorization**: After multiple incorrect attempts, the admin can unlock the app with a master password (default: `admin123`).

## 🧩 **How It Works**

### 🔑 **Key and Cipher Generation**
- A unique encryption key is generated using **Fernet** (from the `cryptography` library), which is used to encrypt and decrypt the data.

### 🧳 **Passkey Hashing**
- The passkey provided by the user is hashed using **SHA-256** for secure storage and comparison.

### 🔒 **Data Encryption and Decryption**
- When the user inputs data, it is encrypted with the generated key. The encrypted data and the hashed passkey are stored.
- When retrieving the data, the user must provide the identifier and passkey. If the passkey is correct, the data is decrypted.

### 🚫 **Lock Access & Reauthorization**
- After 3 incorrect passkey attempts, the app locks the user out. To unlock, the admin needs to enter the master password (`admin123` by default).

## ⚠️ **Troubleshooting**

- **Incorrect Passkey**: Ensure you enter the correct passkey. If you exceed 3 failed attempts, reauthorize through the login page.
- **No Identifier Found**: Ensure the identifier is correct. If it doesn't exist, no data will be retrieved.
