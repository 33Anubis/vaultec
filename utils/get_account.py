from utils.vault_utils import load_vault
from utils.crypto_utils import derive_fernet_key, hash_password, decrypt
from InquirerPy import inquirer
from cryptography.fernet import Fernet
from getpass import getpass


def get_account(domain):
    vault = load_vault()

    salt = bytes.fromhex(vault["master"]["salt"])
    stored_hash = bytes.fromhex(vault["master"]["hash"])

    master_pw = getpass("Enter your master password: ")
    if hash_password(master_pw, salt) != stored_hash:
        print("❌ Access denied.")
        return

    key = derive_fernet_key(master_pw, salt)
    fernet = Fernet(key)

    entries = vault.get("entries", {})

    if domain not in entries or not entries[domain]:
        print(f"No accounts found under '{domain}'.")
        return

    choices = [account["username"] for account in entries[domain]]

    selected = inquirer.select(
        message=f"Select account under '{domain}':", choices=choices
    ).execute()

    # Find selected account
    for acc in entries[domain]:
        if acc["username"] == selected:
            decrypted_pw = decrypt(fernet, acc["password"])
            print(f"\n🔐 Password for {selected}: {decrypted_pw}\n")
            return

    print("Account not found. This shouldn't happen.")
