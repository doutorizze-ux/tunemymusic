import os
from dotenv import load_dotenv

print(f"Current working directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

load_dotenv(override=True)
secret_key = os.getenv("SECRET_KEY")
print(f"SECRET_KEY loaded: {secret_key}")

if not secret_key:
    print("ERROR: SECRET_KEY is None or empty")
else:
    print("SUCCESS: SECRET_KEY found")
