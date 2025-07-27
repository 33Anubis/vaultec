from rich import print
from pyfiglet import Figlet
def help():

    figlet = Figlet(font="slant")
    print(f"[cyan]{figlet.renderText('Vaultec')}[/cyan]")

    print("Usage:")
    print("  --init             Initialize a new vault")
    print("  --add <domain> <email>")
    print("  --get <domain>     Manage accounts for domain")
    print("  --browse           View all domains & accounts")
    print("  --update-mpw       Update master password")
    print("  --reset            Reset the vault")
    print("  --help / -h        View insturctions")
