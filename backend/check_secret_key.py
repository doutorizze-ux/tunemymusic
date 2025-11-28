import os
from dotenv import load_dotenv

load_dotenv(override=True)

secret_key = os.getenv("SECRET_KEY")
print(f"SECRET_KEY present: {bool(secret_key)}")
if secret_key:
    print(f"SECRET_KEY length: {len(secret_key)}")
