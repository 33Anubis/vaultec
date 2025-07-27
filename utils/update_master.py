from getpass import getpass
from utils.vault_utils import load_vault, save_vault
from utils.crypto_utils import derive_fernet_key, hash_password, decrypt, encrypt
from cryptography.fernet import Fernet
from rich import print
import os


def update_master_password():
    vault = load_vault()

    old_salt = bytes.fromhex(vault["master"]["salt"])
    old_hash = bytes.fromhex(vault["master"]["hash"])

    old_pw = getpass("Enter current master password: ")
    if hash_password(old_pw, old_salt) != old_hash:
        print("[bold red]❌ Incorrect password.[/bold red]")
        return

    # 1: Confirm new password
    while True:
        new_pw1 = getpass("Enter NEW master password (8+ chars): ")
        if len(new_pw1) < 8:
            print("Password too short.")
            continue
        new_pw2 = getpass("Confirm NEW master password: ")
        if new_pw1 != new_pw2:
            print("Passwords don't match. Try again.")
            continue
        break

    # 2: Re-encrypt entries
    old_key = Fernet(derive_fernet_key(old_pw, old_salt))
    new_salt = os.urandom(16)
    new_key = Fernet(derive_fernet_key(new_pw1, new_salt))

    for domain in vault["entries"]:
        for acc in vault["entries"][domain]:
            decrypted_pw = decrypt(old_key, acc["password"])
            acc["password"] = encrypt(new_key, decrypted_pw)

    # 3: Update vault meta
    vault["master"]["salt"] = new_salt.hex()
    vault["master"]["hash"] = hash_password(new_pw1, new_salt).hex()

    save_vault(vault)
    print("[bold green]✅ Master password updated successfully.[/bold green]")
