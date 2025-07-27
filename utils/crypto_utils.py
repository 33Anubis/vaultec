import os
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64


def generate_salt():
    return os.urandom(16)


def hash_password(password, salt, iterations=100_000):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def derive_fernet_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def decrypt(fernet, ciphertext: str) -> str:
    return fernet.decrypt(ciphertext.encode()).decode()
