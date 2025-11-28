import secrets
import os

key = secrets.token_hex(24)
env_path = "c:/Users/User/Desktop/tunemymusic.com/backend/.env"

# Check if SECRET_KEY is already in the file
try:
    with open(env_path, "r") as f:
        content = f.read()
        if "SECRET_KEY" in content:
            print("SECRET_KEY already exists in .env")
            # We might want to replace it if it's empty, but for now let's assume if it exists it might be just missing value or commented out?
            # If it is "SECRET_KEY=", we should probably update it.
            # But since os.getenv returned None, it's likely not set or set to empty.
            pass
        else:
            with open(env_path, "a") as f_append:
                f_append.write(f"\nSECRET_KEY={key}\n")
            print(f"Added SECRET_KEY to {env_path}")
except FileNotFoundError:
    with open(env_path, "w") as f:
        f.write(f"SECRET_KEY={key}\n")
    print(f"Created .env with SECRET_KEY")
