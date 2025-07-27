from utils.vault_utils import load_vault, save_vault
from utils.crypto_utils import derive_fernet_key, decrypt, encrypt, hash_password
from InquirerPy import inquirer
from cryptography.fernet import Fernet
from getpass import getpass


def browse_vault():
    vault = load_vault()

    # Get master password
    salt = bytes.fromhex(vault["master"]["salt"])
    stored_hash = bytes.fromhex(vault["master"]["hash"])

    master_pw = getpass("Enter your master password: ")
    if hash_password(master_pw, salt) != stored_hash:
        print("❌ Access denied.")
        return

    fernet = Fernet(derive_fernet_key(master_pw, salt))

    while True:
        domains = list(vault["entries"].keys())
        if not domains:
            print("No domains found in your vault.")
            return

        selected_domain = inquirer.select(
            message="Select a domain (or press Esc to exit):",
            choices=domains + ["[Exit]"],
        ).execute()

        if selected_domain == "[Exit]":
            break

        accounts = vault["entries"].get(selected_domain, [])
        if not accounts:
            print(f"No accounts found under {selected_domain}.")
            continue

        while True:
            account_choices = [acc["username"] for acc in accounts] + ["[Back]"]
            selected_account = inquirer.select(
                message=f"Accounts under '{selected_domain}':", choices=account_choices
            ).execute()

            if selected_account == "[Back]":
                break

            account = next(
                acc for acc in accounts if acc["username"] == selected_account
            )

            action = inquirer.select(
                message=f"What would you like to do with '{selected_account}'?",
                choices=[
                    "View password",
                    "Update password",
                    "Delete account",
                    "[Back]",
                ],
            ).execute()

            if action == "View password":
                pw = decrypt(fernet, account["password"])
                print(f"🔐 Password for {selected_account}: {pw}\n")

            elif action == "Update password":
                new_pw = getpass("Enter new password: ")
                account["password"] = encrypt(fernet, new_pw)
                save_vault(vault)
                print("✅ Password updated.")

            elif action == "Delete account":
                confirm = input(
                    f"Are you sure you want to delete '{selected_account}'? (y/n): "
                )
                if confirm.lower() == "y":
                    accounts.remove(account)
                    save_vault(vault)
                    print("✅ Account deleted.")
                    break  # Go back to account list

            elif action == "[Back]":
                continue
