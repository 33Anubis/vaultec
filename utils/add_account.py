from cryptography.fernet import Fernet
from utils.crypto_utils import derive_fernet_key
from getpass import getpass


def add_account(vault, domain, username, master_password, salt):
    entries = vault.get("entries", {})

    if domain not in entries:
        entries[domain] = []

    domain_entries = entries[domain]

    # Check if this username already exists
    for account in domain_entries:
        if account["username"] == username:
            overwrite = input(
                f"Account '{username}' already exists under '{domain}'. Overwrite password? (y/n): "
            )
            if overwrite.lower() != "y":
                print("Aborted.")
                return
            break

    # Prompt for password
    pw = getpass("Enter the password to store: ")

    # Derive Fernet key and encrypt
    key = derive_fernet_key(master_password, salt)
    fernet = Fernet(key)
    encrypted_pw = fernet.encrypt(pw.encode()).decode()

    # Update or add new
    for account in domain_entries:
        if account["username"] == username:
            account["password"] = encrypted_pw
            break
    else:
        domain_entries.append({"username": username, "password": encrypted_pw})

    entries[domain] = domain_entries
    vault["entries"] = entries

    print(f"✅ Password for {username} under {domain} saved.")
