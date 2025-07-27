# This module will check password length

from getpass import getpass
from InquirerPy import inquirer
from utils.generate_password import generate_password
from rich import print


def prompt_password():
    auto = inquirer.confirm(
        message="Generate a strong password automatically?", default=True
    ).execute()

    if auto:
        return generate_password()

    while True:
        pw = getpass("Enter password (8+ chars): ")
        if len(pw) < 8:
            print("[bold red]❌ Password too short.[/bold red]")
            continue
        return pw
