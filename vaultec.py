import sys
from utils.verify_vault import verify_and_unlock_vault
from utils.vault_init import vault_init
from utils.add_account import add_account
from utils.vault_utils import save_vault
from utils.get_account import get_account
from utils.update_master import update_master_password
from utils.reset_vault import reset_vault
from utils.browse_vault import browse_vault
from utils.help import help
from rich import print
from rich.panel import Panel


def main():
    banner = print(Panel("Welcome to [bold cyan]Vaultec[/bold cyan] 🔐", style="blue"))

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "--init":
            banner
            vault_init()
        elif cmd == "--verify":
            banner
            verify_and_unlock_vault()
        elif cmd == "--add":
            banner
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
            banner
            if len(sys.argv) < 3:
                print("Usage: get <domain>")
                return

            domain = sys.argv[2]
            get_account(domain)
        elif cmd == "--update-mpw":
            banner
            if len(sys.argv) != 2:
                print("Usage: --update-mpw")
                return
            update_master_password()
        elif cmd == "--reset":
            banner
            if len(sys.argv) != 2:
                print("Usage: --reset")
                return
            reset_vault()
        elif cmd == "--browse":
            banner
            if len(sys.argv) != 2:
                print("Usage: --browse")
                return
            browse_vault()
        elif cmd == "--help" or cmd == "-h":
            help()
        else:
            print(f"Unknown command: {cmd}")
            print("Use '--help' or '-h' to view instructions")
    else:
        help()
    print("\nVersion 1.0 | Created by Michael Zakhary")


if __name__ == "__main__":
    main()
