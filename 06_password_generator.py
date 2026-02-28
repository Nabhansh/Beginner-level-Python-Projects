# ============================================================
# PROJECT 6: Random Password Generator
# ============================================================

import random
import string
import re

def check_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:   score += 1
    else: feedback.append("Use at least 8 characters")

    if len(password) >= 12:  score += 1
    if len(password) >= 16:  score += 1

    if re.search(r'[A-Z]', password): score += 1
    else: feedback.append("Add uppercase letters")

    if re.search(r'[a-z]', password): score += 1
    else: feedback.append("Add lowercase letters")

    if re.search(r'\d', password):    score += 1
    else: feedback.append("Add numbers")

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 1
    else: feedback.append("Add special characters")

    if score <= 2:   strength, color = "Weak 🔴",   "Weak"
    elif score <= 4: strength, color = "Fair 🟡",   "Fair"
    elif score <= 6: strength, color = "Strong 🟢", "Strong"
    else:            strength, color = "Very Strong 💪", "Very Strong"

    return strength, feedback

def generate_password(length=12, use_upper=True, use_lower=True,
                       use_digits=True, use_symbols=True, exclude_ambiguous=False):
    characters = ""
    required = []

    ambiguous = "il1Lo0O"

    if use_lower:
        chars = string.ascii_lowercase
        if exclude_ambiguous:
            chars = ''.join(c for c in chars if c not in ambiguous)
        characters += chars
        required.append(random.choice(chars))

    if use_upper:
        chars = string.ascii_uppercase
        if exclude_ambiguous:
            chars = ''.join(c for c in chars if c not in ambiguous)
        characters += chars
        required.append(random.choice(chars))

    if use_digits:
        chars = string.digits
        if exclude_ambiguous:
            chars = ''.join(c for c in chars if c not in ambiguous)
        characters += chars
        required.append(random.choice(chars))

    if use_symbols:
        chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        characters += chars
        required.append(random.choice(chars))

    if not characters:
        return None

    remaining_len = length - len(required)
    if remaining_len < 0:
        remaining_len = 0

    password_chars = required + [random.choice(characters) for _ in range(remaining_len)]
    random.shuffle(password_chars)
    return ''.join(password_chars)

def main():
    print("=" * 50)
    print("     🔐 RANDOM PASSWORD GENERATOR")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("  1. Generate password with custom settings")
        print("  2. Quick generate (strong 16-char password)")
        print("  3. Generate multiple passwords")
        print("  4. Check password strength")
        print("  5. Quit")
        choice = input("\nChoose: ").strip()

        if choice == '1':
            try:
                length = int(input("Password length (8-64): ").strip())
                length = max(8, min(64, length))
            except ValueError:
                length = 16
            use_upper   = input("Include uppercase? (y/n, default=y): ").lower() != 'n'
            use_lower   = input("Include lowercase? (y/n, default=y): ").lower() != 'n'
            use_digits  = input("Include digits?    (y/n, default=y): ").lower() != 'n'
            use_symbols = input("Include symbols?   (y/n, default=y): ").lower() != 'n'
            exclude_amb = input("Exclude ambiguous chars (0,O,l,1)? (y/n): ").lower() == 'y'

            pwd = generate_password(length, use_upper, use_lower, use_digits, use_symbols, exclude_amb)
            if pwd:
                strength, tips = check_strength(pwd)
                print(f"\n  ✅ Password: {pwd}")
                print(f"  📊 Strength: {strength}")
                if tips:
                    print(f"  💡 Tips: {', '.join(tips)}")
            else:
                print("  ❌ Please select at least one character type!")

        elif choice == '2':
            pwd = generate_password(16)
            strength, _ = check_strength(pwd)
            print(f"\n  ✅ Password: {pwd}")
            print(f"  📊 Strength: {strength}")

        elif choice == '3':
            try:
                count = int(input("How many passwords? (1-20): "))
                count = max(1, min(20, count))
                length = int(input("Length (default=12): ") or "12")
            except ValueError:
                count, length = 5, 12
            print(f"\n  Generated {count} passwords:")
            print("  " + "-" * 40)
            for i in range(count):
                pwd = generate_password(length)
                strength, _ = check_strength(pwd)
                print(f"  {i+1:2}. {pwd}  [{strength}]")

        elif choice == '4':
            pwd = input("Enter password to check: ")
            strength, tips = check_strength(pwd)
            print(f"\n  📊 Strength: {strength}")
            if tips:
                print("  💡 Suggestions:")
                for tip in tips:
                    print(f"    • {tip}")
            else:
                print("  ✅ Excellent password!")

        elif choice == '5':
            print("\nStay secure! 🔒")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
