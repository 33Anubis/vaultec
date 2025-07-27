from cryptography.fernet import Fernet
from utils.crypto_utils import derive_fernet_key
from getpass import getpass
from InquirerPy import inquirer
from utils.generate_password import generate_password
from rich import print


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

    # Ask if user wants to generate a password
    use_generator = inquirer.confirm(
        message="Generate a strong password automatically?", default=True
    ).execute()

    if use_generator:
        pw = generate_password()

        # Optional: Show user and let them copy it
        show_pw = inquirer.confirm(
            message="Show the generated password?", default=True
        ).execute()

        if show_pw:
            print(f"\n📋 Copy this password now: {pw}\n")
    else:
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

    print(f"[bold green]✅ Password for[/bold green] [cyan]{username}[/cyan] [bold green]under[/bold green] [magenta]{domain}[/magenta] [bold green]saved.[/bold green]")
