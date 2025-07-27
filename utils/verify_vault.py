from getpass import getpass
from utils.crypto_utils import hash_password
from utils.vault_utils import vault_exists, load_vault


def verify_and_unlock_vault():
    if not vault_exists():
        print("Vault not found. Please initialize with '--init'.")
        return None, None, None  # vault, password, salt

    vault = load_vault()
    salt = bytes.fromhex(vault["master"]["salt"])
    stored_hash = bytes.fromhex(vault["master"]["hash"])

    entered_pw = getpass("Enter your master password: ")
    hashed_attempt = hash_password(entered_pw, salt)

    if hashed_attempt != stored_hash:
        print("❌ Access denied.")
        return None, None, None

    print("✅ Access granted.")
    return vault, entered_pw, salt
