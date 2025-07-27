import os
import json

VAULT_PATH = "vault.json"


def vault_exists():
    return os.path.exists(VAULT_PATH)


def load_vault():
    with open(VAULT_PATH, "r") as f:
        return json.load(f)


def save_vault(data):
    with open(VAULT_PATH, "w") as f:
        json.dump(data, f, indent=2)
