import secrets
import string

print("=== Python Password Generator ===\n")

# 1. Get user preferences
length = int(input("Enter desired password length (e.g., 12): "))
use_numbers = input("Include numbers? (y/n): ").lower() == "y"
use_symbols = input("Include symbols? (y/n): ").lower() == "y"

# 2. Build the character pool
characters = string.ascii_letters  # Starts with a-z and A-Z

if use_numbers:
    characters += string.digits  # Adds 0-9
if use_symbols:
    characters += string.punctuation  # Adds !@#$%^&*(), etc.

# 3. Generate the password securely
password_chars = []
for _ in range(length):
    random_char = secrets.choice(characters)
    password_chars.append(random_char)

password = "".join(password_chars)

print(f"\nYour generated password: {password}")