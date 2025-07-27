import sys
from utils.verify_vault import verify_and_unlock_vault
from utils.vault_init import vault_init
from utils.add_account import add_account
from utils.vault_utils import save_vault
from utils.get_account import get_account


def main():
    print("Welcome to Vaultec 🔐\n")

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "--init":
            vault_init()
        elif cmd == "--verify":
            verify_and_unlock_vault()
        elif cmd == "--add":
            if len(sys.argv) < 4:
                print("Usage: add <domain> <username>")
                return

            domain = str(sys.argv[2])
            username = str(sys.argv[3])

            vault, master_pw, salt = verify_and_unlock_vault()
            if not vault:
                return

            add_account(vault, domain, username, master_pw, salt)
            save_vault(vault)
        elif cmd == "--get":
            if len(sys.argv) < 3:
                print("Usage: get <domain>")
                return

            domain = sys.argv[2]
            get_account(domain)
        else:
            print(f"Unknown command: {cmd}")
    else:
        print("Usage:")
        print("  --init     Initialize a new vault")
        print("  --verify   Verify master password")
        print("  --add <domain_name> <account@domain.com>")
        print("  --get <domain_name> View, Update, Delete accounts")


if __name__ == "__main__":
    main()
