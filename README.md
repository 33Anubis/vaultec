# 🔐 Vaultec

Vaultec is a lightweight, offline-first command-line password manager built with Python.

It uses strong encryption to safely store multiple account credentials per domain, all protected by a master password you control.

No cloud. No telemetry. Just secure local storage, with a clean CLI UI.

# 🔧 Features (v0.1)
🔑 Master password with salted hashing

🔐 Encrypted local vault (AES via Fernet)

👥 Multiple accounts per domain

🧭 Interactive CLI with arrow-key navigation

🎲 Random password generation with custom rules (pawssword length, with(out) numbers, with(out) special characters)

🔄 Change or update credentials per account, per domain and master password

> ⚠️ Still in development – use at your own risk. Not intended for production or sensitive info (yet).

# 🛠️ Quick Setup
bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python vaultec.py --init

# What I Learned
____
## From boot.dev
1.
2.

## From research during this project
1.
2.