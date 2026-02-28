# ============================================================
# PROJECT 14: Email Slicer
# ============================================================

import re
import json
import os
from collections import Counter

FAMOUS_PROVIDERS = {
    "gmail.com": "Google Gmail", "yahoo.com": "Yahoo Mail",
    "outlook.com": "Microsoft Outlook", "hotmail.com": "Microsoft Hotmail",
    "live.com": "Microsoft Live", "icloud.com": "Apple iCloud",
    "me.com": "Apple Me", "mac.com": "Apple Mac",
    "protonmail.com": "ProtonMail", "proton.me": "ProtonMail",
    "aol.com": "AOL Mail", "zoho.com": "Zoho Mail",
    "yandex.com": "Yandex Mail", "gmx.com": "GMX Mail",
    "tutanota.com": "Tutanota", "fastmail.com": "Fastmail",
}

def validate_email(email):
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def slice_email(email):
    """Extract all information from an email address."""
    email = email.strip().lower()
    if not validate_email(email):
        return None

    username, domain = email.split('@', 1)
    domain_name, *tld_parts = domain.rsplit('.', 1)
    tld = tld_parts[0] if tld_parts else ""

    # Username analysis
    has_dots   = '.' in username
    has_nums   = any(c.isdigit() for c in username)
    has_plus   = '+' in username   # Gmail alias trick
    has_under  = '_' in username
    has_hyphen = '-' in username

    # Possible name from username
    clean_name = re.sub(r'[._+\-]', ' ', username)
    clean_name = re.sub(r'\d+', '', clean_name).strip().title()

    provider = FAMOUS_PROVIDERS.get(domain, f"Unknown ({domain})")

    return {
        "email": email,
        "username": username,
        "domain": domain,
        "domain_name": domain_name,
        "tld": tld,
        "provider": provider,
        "is_known_provider": domain in FAMOUS_PROVIDERS,
        "username_analysis": {
            "length": len(username),
            "has_dots": has_dots,
            "has_numbers": has_nums,
            "has_plus_alias": has_plus,
            "has_underscore": has_under,
            "has_hyphen": has_hyphen,
            "possible_name": clean_name if clean_name else "N/A"
        }
    }

def display_email_info(info):
    """Display formatted email information."""
    print(f"\n{'='*55}")
    print(f"  📧 EMAIL ANALYSIS")
    print(f"{'='*55}")
    print(f"  Full Email:    {info['email']}")
    print(f"  Username:      {info['username']}")
    print(f"  Domain:        {info['domain']}")
    print(f"  Domain Name:   {info['domain_name']}")
    print(f"  TLD:           .{info['tld']}")
    print(f"  Provider:      {info['provider']}")
    print(f"  Known Service: {'✅ Yes' if info['is_known_provider'] else '❌ No (custom/corporate)'}")

    ua = info['username_analysis']
    print(f"\n  Username Analysis:")
    print(f"  ├─ Length:       {ua['length']} characters")
    print(f"  ├─ Has Numbers:  {'Yes' if ua['has_numbers'] else 'No'}")
    print(f"  ├─ Has Dots:     {'Yes' if ua['has_dots'] else 'No'}")
    print(f"  ├─ Has Alias (+):{'Yes (Gmail trick!)' if ua['has_plus_alias'] else 'No'}")
    print(f"  └─ Likely Name:  {ua['possible_name']}")
    print(f"{'='*55}")

def analyze_bulk_emails(emails):
    """Analyze a list of email addresses."""
    valid_infos = []
    invalid = []

    for email in emails:
        email = email.strip()
        if not email:
            continue
        if validate_email(email):
            info = slice_email(email)
            if info:
                valid_infos.append(info)
        else:
            invalid.append(email)

    print(f"\n{'='*55}")
    print(f"  📊 BULK ANALYSIS RESULTS")
    print(f"{'='*55}")
    print(f"  Total processed: {len(emails)}")
    print(f"  Valid:           {len(valid_infos)} ✅")
    print(f"  Invalid:         {len(invalid)} ❌")

    if valid_infos:
        # Provider stats
        providers = Counter(info['domain'] for info in valid_infos)
        print(f"\n  📈 Top Email Providers:")
        for provider, count in providers.most_common(5):
            bar = '█' * min(count * 3, 20)
            name = FAMOUS_PROVIDERS.get(provider, provider)
            print(f"  {name:20s} {bar} {count}")

        # TLD stats
        tlds = Counter(info['tld'] for info in valid_infos)
        print(f"\n  🌍 Top TLDs:")
        for tld, count in tlds.most_common(5):
            print(f"  .{tld:10s} {count} emails")

    if invalid:
        print(f"\n  ❌ Invalid emails:")
        for e in invalid:
            print(f"  • {e}")

    return valid_infos, invalid

def main():
    print("=" * 55)
    print("          ✂️  EMAIL SLICER")
    print("=" * 55)

    history = []

    while True:
        print("\nOptions:")
        print("  1. 📧 Analyze single email")
        print("  2. 📋 Analyze multiple emails")
        print("  3. 📂 Analyze from file (emails.txt)")
        print("  4. 🕐 View history")
        print("  5. 💾 Export history to JSON")
        print("  6. 🧹 Clear history")
        print("  7. 🚪 Quit")

        choice = input("\nChoose: ").strip()

        if choice == '1':
            email = input("  Enter email address: ").strip()
            info = slice_email(email)
            if info:
                display_email_info(info)
                history.append(info)
            else:
                print(f"  ❌ '{email}' is not a valid email address!")
                print("  Example of valid email: user@example.com")

        elif choice == '2':
            print("  Enter email addresses (one per line).")
            print("  Type 'done' on a new line when finished:\n")
            emails = []
            while True:
                line = input("  > ").strip()
                if line.lower() == 'done':
                    break
                emails.append(line)
            if emails:
                valid, _ = analyze_bulk_emails(emails)
                history.extend(valid)

        elif choice == '3':
            filename = input("  Filename (default: emails.txt): ").strip() or "emails.txt"
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    emails = [line.strip() for line in f if line.strip()]
                print(f"  📂 Loaded {len(emails)} lines from {filename}")
                valid, _ = analyze_bulk_emails(emails)
                history.extend(valid)
            else:
                print(f"  ❌ File '{filename}' not found.")
                print("  Create a text file with one email per line.")

        elif choice == '4':
            if not history:
                print("  No history yet.")
            else:
                print(f"\n  📜 Analyzed emails ({len(history)}):")
                print(f"  {'─'*50}")
                for i, info in enumerate(history, 1):
                    name = info['username_analysis']['possible_name']
                    print(f"  {i:3}. {info['email']:35s} → {name}")

        elif choice == '5':
            if history:
                with open("email_analysis.json", 'w') as f:
                    json.dump(history, f, indent=2)
                print("  ✅ Saved to email_analysis.json")
            else:
                print("  No data to export!")

        elif choice == '6':
            history.clear()
            print("  ✅ History cleared.")

        elif choice == '7':
            print("\n  👋 Goodbye!")
            break
        else:
            print("  Invalid choice!")

if __name__ == "__main__":
    main()
