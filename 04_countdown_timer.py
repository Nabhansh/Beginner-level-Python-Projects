# ============================================================
# PROJECT 4: Countdown Timer
# ============================================================

import time
import sys

def countdown(seconds):
    print("\n" + "=" * 35)
    print("       ⏱  COUNTDOWN TIMER")
    print("=" * 35)
    total = seconds
    try:
        while seconds >= 0:
            hrs = seconds // 3600
            mins = (seconds % 3600) // 60
            secs = seconds % 60
            progress = int(30 * (total - seconds) / total) if total > 0 else 30
            bar = "█" * progress + "░" * (30 - progress)
            timer_display = f"  ⏳ {hrs:02d}:{mins:02d}:{secs:02d}  "
            sys.stdout.write(f"\r{timer_display}  [{bar}]")
            sys.stdout.flush()
            time.sleep(1)
            seconds -= 1

        print("\n\n  🔔 TIME'S UP! 🔔")
        print("=" * 35)
        # Bell sound
        print("\a")

    except KeyboardInterrupt:
        print("\n\n  ⏹ Timer cancelled.")

def parse_time_input(user_input):
    """Parse inputs like '90', '1:30', '1h30m', '01:30:00'"""
    user_input = user_input.strip().lower()
    # HH:MM:SS or MM:SS
    if ':' in user_input:
        parts = user_input.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    # Like "1h30m10s"
    total = 0
    import re
    h = re.search(r'(\d+)h', user_input)
    m = re.search(r'(\d+)m', user_input)
    s = re.search(r'(\d+)s', user_input)
    if h: total += int(h.group(1)) * 3600
    if m: total += int(m.group(1)) * 60
    if s: total += int(s.group(1))
    if total: return total
    # Plain seconds
    return int(user_input)

def main():
    print("=" * 35)
    print("       ⏱  COUNTDOWN TIMER")
    print("=" * 35)
    print("Format examples:")
    print("  90        → 90 seconds")
    print("  1:30      → 1 min 30 sec")
    print("  1h30m     → 1 hour 30 min")
    print("  01:30:00  → 1 hour 30 min")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("Enter time: ").strip()
        if user_input.lower() == 'quit':
            break
        try:
            seconds = parse_time_input(user_input)
            if seconds <= 0:
                print("Please enter a positive time!\n")
                continue
            hrs = seconds // 3600
            mins = (seconds % 3600) // 60
            secs = seconds % 60
            print(f"\nStarting countdown: {hrs:02d}:{mins:02d}:{secs:02d}")
            countdown(seconds)
            again = input("\nStart another timer? (y/n): ").strip().lower()
            if again != 'y':
                break
        except ValueError:
            print("Invalid time format. Try again.\n")

if __name__ == "__main__":
    main()
