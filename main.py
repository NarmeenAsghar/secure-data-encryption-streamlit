# imports
import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# --- 1. Generate Key and Cipher ---
# Generate a unique encryption key using Fernet
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# --- 2. Session State Initialization ---
# Initialize session variables to track failed attempts, authorization, and stored data
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "authorized" not in st.session_state:
    st.session_state.authorized = True
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}

# --- 3. Helper Functions ---
# Function to hash the passkey using SHA-256
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Function to encrypt the input text using the generated cipher
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# Function to decrypt the encrypted text using the passkey
def decrypt_data(encrypted_text, passkey):
    hashed = hash_passkey(passkey)
# Check if the encrypted text matches the stored one, and if passkey is correct
    for record in st.session_state.stored_data.values():
        if record["encrypted_text"] == encrypted_text:
            if record["passkey"] == hashed:
                st.session_state.failed_attempts = 0  # Reset failed attempts on success
                return cipher.decrypt(encrypted_text.encode()).decode()
            break
    st.session_state.failed_attempts += 1  # Increment failed attempts if wrong passkey
    return None

# --- 4. Sidebar Navigation ---
# Sidebar menu for navigation
with st.sidebar:
    st.title("🔐 Secure Vault")
    st.markdown("Navigate through:")
    menu = ["🏠 Home", "📂 Store Data", "🔍 Retrieve Data", "🔑 Login"]
    choice = st.radio("Menu", menu)

# --- 5. Home Page ---
# Home page content description
if choice == "🏠 Home":
    st.title("🏠 Welcome to Secure Data Encryption")
    st.markdown("""
    This app helps you:
    - 🔐 **Encrypt and Store Confidential Data**
    - 🔓 **Retrieve it using a Passkey**
    - 🚫 **Lock Access after Multiple Failed Attempts**
    """)
    st.info("Use the sidebar menu to explore features.")

# --- 6. Store Data Page ---
# Page to encrypt and store data securely
elif choice == "📂 Store Data":
    st.title("📂 Secure Data Entry")

    st.markdown("### 🔑 Add New Encrypted Entry")
    col1, col2 = st.columns(2)
    with col1:
        identifier = st.text_input("🆔 Unique Identifier")  # Input for unique identifier
    with col2:
        passkey = st.text_input("🔑 Passkey", type="password")  # Input for passkey

    user_data = st.text_area("📝 Enter the text to be encrypted", height=150)  # Text input to be encrypted

    if st.button("🔒 Encrypt & Store"):
        if identifier and user_data and passkey:  # Check if all fields are filled
            if identifier in st.session_state.stored_data:
                st.warning("⚠️ Identifier already exists. Choose a new one.")  # Warning if identifier exists
            else:
                encrypted = encrypt_data(user_data)  # Encrypt the data
                hashed = hash_passkey(passkey)  # Hash the passkey
                # Store the encrypted data and the hashed passkey
                st.session_state.stored_data[identifier] = {
                    "encrypted_text": encrypted,
                    "passkey": hashed
                }
                st.success("✅ Successfully encrypted and stored!")  # Success message
                with st.expander("📦 View Encrypted Data"):
                    st.code(encrypted, language="text")  # Show encrypted data
        else:
            st.error("❌ Please complete all fields.")  # Error if fields are incomplete

# --- 7. Retrieve Data Page ---
# Page to retrieve and decrypt stored data
elif choice == "🔍 Retrieve Data":
    if not st.session_state.authorized:
        st.warning("🔒 Access locked after multiple failed attempts.")  # Lock message after failed attempts
        st.info("🔁 Go to 'Login' page to reauthorize.")
        st.stop()

    st.title("🔍 Retrieve Stored Data")
    st.markdown("Provide your identifier and passkey to decrypt the message.")

    col1, col2 = st.columns(2)
    with col1:
        identifier = st.text_input("🆔 Identifier")  # Input for identifier
    with col2:
        passkey = st.text_input("🔑 Passkey", type="password")  # Input for passkey

    if st.button("🔓 Decrypt"):
        if identifier and passkey:  # Check if all fields are filled
            if identifier in st.session_state.stored_data:
                encrypted_text = st.session_state.stored_data[identifier]["encrypted_text"]  # Get encrypted text
                decrypted = decrypt_data(encrypted_text, passkey)  # Decrypt the data
                if decrypted:
                    st.success("✅ Decryption successful!")  # Show decrypted data
                    st.code(decrypted, language="text")
                else:
                    attempts_left = 3 - st.session_state.failed_attempts  # Show remaining attempts
                    st.error(f"❌ Wrong passkey! Attempts remaining: {attempts_left}")
                    if st.session_state.failed_attempts >= 3:
                        st.session_state.authorized = False  # Lock access after 3 failed attempts
                        st.warning("🔒 Too many attempts. Redirecting...")
                        st.experimental_rerun()  # Reload page
            else:
                st.error("⚠️ No such identifier found.")  # Error if identifier doesn't exist
        else:
            st.error("❌ All fields must be filled.")  # Error if fields are incomplete

# --- 8. Login Page ---
# Page to reauthorize after access is locked
elif choice == "🔑 Login":
    st.title("🔐 Admin Reauthorization")
    st.markdown("Access is locked after multiple incorrect attempts. Reauthorize below:")

    master_pass = st.text_input("🔑 Master Password", type="password")  # Input for master password

    if st.button("🔓 Reauthorize"):
        if master_pass == "admin123":  # Check if master password is correct (hardcoded for demo)
            st.session_state.failed_attempts = 0  # Reset failed attempts
            st.session_state.authorized = True  # Grant access again
            st.success("✅ Access restored. Try again from Retrieve Data.")  # Success message
        else:
            st.error("❌ Incorrect master password.")  # Error for incorrect password
