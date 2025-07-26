import json
import os
import sys
from getpass import getpass
import hashlib


def main():
    print("Welcome to Vaultec 🔐.")
    print("")

    # Created this to not DRY
    def exit_logic(key):
        if str(key).lower() == "q":
            sys.exit(1)
    
    def reenter_logic(key):
        if str(key).lower() == "p":
            print("Resetting master password.")
            return True
        return False

    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        if os.path.exists("vault.json"):
            print("Vault already exists. Initialization skipped.")
            sys.exit(1)
        else:
            # initializing the two pw attempts to two diff values so the while loop can be entered
            # I had a bug here where I set both to None so the while loop was being skipped
            pw1, pw2 = "", " "
            while pw1 != pw2:
                pw1 = getpass("Set master password (8 characters minimum): ")

                if len(pw1) < 8:
                    print(
                        "\nPassword must be at least 8 characters.\n" \
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
                        "I. Enter 'q' + enter to exit.\n" \
                        "II. Press 'Enter' to input the confirmation password again.\n" \
                        "III. Enter 'p' + enter to re-enter your password from the start."
                    )
                        key = input()
                        #if q is selected, quit
                        exit_logic(key)
                        #if p is selected, reattempt confirmation password only
                        if reenter_logic(key):
                            break

            # generate salt and hash
            salt = os.urandom(16)
            hashed_pw = hashlib.pbkdf2_hmac(
                "sha256", pw1.encode("utf-8"), salt, 100_000
            )

            # store in JSON + JSON structure
            vault_data = {
                "master": {"salt": salt.hex(), "hash": hashed_pw.hex()},
                "entries": {},
            }

            # Create JSON vault
            with open("vault.json", "w") as f:
                json.dump(vault_data, f, indent=2)

            print("Vault initialized successfully.")

    else:
        print("Run with '--init' to set up your vault.")


if __name__ == "__main__":
    main()
