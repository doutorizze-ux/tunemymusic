import os
from dotenv import load_dotenv

load_dotenv(override=True)

google_client_id = os.getenv("GOOGLE_CLIENT_ID")
google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
google_redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

print(f"GOOGLE_CLIENT_ID present: {bool(google_client_id)}")
print(f"GOOGLE_CLIENT_SECRET present: {bool(google_client_secret)}")
print(f"GOOGLE_REDIRECT_URI present: {bool(google_redirect_uri)}")

if google_redirect_uri:
    print(f"GOOGLE_REDIRECT_URI value: {google_redirect_uri}")
