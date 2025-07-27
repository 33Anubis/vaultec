import os
from rich import print


def reset_vault():
    vault_path = "vault.json"

    if not os.path.exists(vault_path):
        print("No vault found to reset.")
        return

    print("⚠️ WARNING: This will permanently delete your vault and all stored accounts.")
    confirm1 = input("Type 'RESET' (case-sensitive) to confirm: ")
    if confirm1 != "RESET":
        print("Reset aborted.")
        return

    confirm2 = input("Are you absolutely sure? Type 'YES' to proceed: ")
    if confirm2 != "YES":
        print("Reset aborted.")
        return

    os.remove(vault_path)
    print("💥 Vault wiped. It's gone. Forever.")
