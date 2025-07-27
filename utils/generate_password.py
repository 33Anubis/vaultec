import random
import string
from InquirerPy import inquirer
from rich import print


def generate_password():
    # Prompt for inputs to determine the totall length and how many digits and how many specials they want
    total_length = 0
    while total_length < 8:
        total_length = int(
            inquirer.number(message="Total password length (8+):", default=12).execute()
        )
        if total_length < 8:
            print("Please select a length of 8 characters or more. 😐\n")

    num_digits = int(
        inquirer.number(
            message="How many digits?", min_allowed=0, max_allowed=total_length
        ).execute()
    )

    num_special = int(
        inquirer.number(
            message="How many special characters?",
            min_allowed=0,
            max_allowed=total_length - num_digits,
        ).execute()
    )

    num_letters = total_length - num_digits - num_special

    if int(num_letters) < 0:
        print("[bold red]❌ Invalid combination. Try again.[/bold red]")
        return generate_password()  # Retry again

    # Character pools
    digits = random.choices(string.digits, k=num_digits)
    specials = random.choices("!@#$%^&*()-_=+[]{}", k=num_special)
    letters = random.choices(string.ascii_letters, k=num_letters)

    all_chars = digits + specials + letters
    random.shuffle(all_chars)

    password = "".join(all_chars)

    return password
