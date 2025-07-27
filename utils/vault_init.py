import sys
from getpass import getpass
from utils.crypto_utils import generate_salt, hash_password
from utils.vault_utils import vault_exists, save_vault
from pyfiglet import Figlet
from rich import print


def vault_init():
    figlet = Figlet(font="slant")
    print(f"[cyan]{figlet.renderText('Vaultec')}[/cyan]")

    if vault_exists():
        print("Vault already exists.")
        return

    # Created this to not DRY
    def exit_logic(key):
        if str(key).lower() == "q":
            sys.exit(1)

    # Created this to no DRY
    def reenter_logic(key):
        if str(key).lower() == "p":
            print("Resetting master password.")
            return True
        return False

    # initializing the two pw attempts to two diff values so the while loop can be entered
    # I had a bug here where I set both to None so the while loop was being skipped
    pw1, pw2 = "", " "
    while pw1 != pw2:
        pw1 = getpass("Set master password (8 characters minimum): ")

        if len(pw1) < 8:
            print(
                "\nPassword must be at least 8 characters.\n"
                "Press 'q' + enter to exit. Please press any other key to try again..."
            )
            key = input()
            exit_logic(key)
            continue

        # checking for password match
        while pw2 != pw1:
            pw2 = getpass("Confirm master password: ")
            if pw2 != pw1:
                print("")
                print("Passwords do not match.")
                print(
                    "Options: \n"
                    "I. Enter 'q' + enter to exit.\n"
                    "II. Press 'Enter' to input the confirmation password again.\n"
                    "III. Enter 'p' + enter to re-enter your password from the start."
                )
                key = input()
                # if q is selected, quit
                exit_logic(key)
                # if p is selected, reattempt confirmation password only
                if reenter_logic(key):
                    break

    # generate salt and hash
    salt = generate_salt()
    hashed_pw = hash_password(pw1, salt)

    # store in JSON + JSON structure
    vault = {
        "master": {"salt": salt.hex(), "hash": hashed_pw.hex()},
        "entries": {},
    }

    # Create JSON vault
    save_vault(vault)

    print("[bold green]Vault initialized successfully.[/bold green]")
