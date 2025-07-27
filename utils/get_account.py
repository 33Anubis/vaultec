from utils.vault_utils import load_vault
from utils.crypto_utils import derive_fernet_key, hash_password, decrypt
from InquirerPy import inquirer
from cryptography.fernet import Fernet
from getpass import getpass
from utils.vault_utils import save_vault


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
    choices.append("Back")

    selected = inquirer.select(
        message=f"Select account under '{domain}':", choices=choices
    ).execute()

    if selected == "Back":
        print("🔙 Returning to main menu.")
        return

    # Find selected account
    for acc in entries[domain]:
        if acc["username"] == selected:
            action = inquirer.select(
                message=f"What would you like to do with '{selected}'?",
                choices=["View password", "Update password", "Delete account", "Back"],
            ).execute()

            if action == "View password":
                decrypted_pw = decrypt(fernet, acc["password"])
                print(f"\n🔐 Password for {selected}: {decrypted_pw}\n")

            elif action == "Update password":
                new_pw = getpass("Enter new password: ")
                encrypted_pw = fernet.encrypt(new_pw.encode()).decode()
                acc["password"] = encrypted_pw
                save_vault(vault)
                print("✅ Password updated.")

            elif action == "Delete account":
                confirm = inquirer.confirm(
                    message=f"Are you sure you want to delete '{selected}'?",
                    default=False,
                ).execute()
                if confirm:
                    entries[domain].remove(acc)
                    save_vault(vault)
                    print("🗑️ Account deleted.")
                else:
                    print("Deletion canceled.")
            else:
                print("Returning.")

            return

    print("Account not found. This shouldn't happen.")
