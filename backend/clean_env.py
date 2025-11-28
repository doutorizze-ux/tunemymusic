import os
import codecs

env_path = "c:/Users/User/Desktop/tunemymusic.com/backend/.env"

# Read with utf-8-sig to handle BOM automatically
try:
    with open(env_path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    
    # Write back with utf-8 (no BOM)
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("Cleaned .env file (removed BOM if present)")
    
    # Verify content
    with open(env_path, "r", encoding="utf-8") as f:
        print("First line:", f.readline())

except Exception as e:
    print(f"Error: {e}")
