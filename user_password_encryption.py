# import modules
from cryptography.fernet import Fernet
import pickle
import os
import subprocess as sp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----- Create encryption engine class

if not os.path.exists(os.path.join(BASE_DIR, "user_password_encryption_key.pickle")):
    key = Fernet.generate_key()  # ----- This is your "password" to unlock and lock files
    # ----- Create a pickle file and dump key into it
    with open(os.path.join(BASE_DIR, 'user_password_encryption_key.pickle'), 'wb') as f:
        pickle.dump(key, f)
    sp.call(["attrib", "+H", f"{os.path.join(BASE_DIR, 'user_password_encryption_key.pickle')}"])


def load_encryption_key_file():
    with open(os.path.join(BASE_DIR, "user_password_encryption_key.pickle"), 'rb') as key_handle:
        encryption_key = pickle.load(key_handle).decode()
        return encryption_key


# This method encode/encrypt text
def encrypt(text):
    cipher_suite = Fernet(load_encryption_key_file())
    encoded_text = cipher_suite.encrypt(text.encode())
    return encoded_text


# This method decode text using the same key used to encrypt it
def decode(encoded_text):
    cipher_suite = Fernet(load_encryption_key_file())
    decoded_text = cipher_suite.decrypt(encoded_text)
    return decoded_text