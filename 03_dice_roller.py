# ============================================================
# PROJECT 3: Dice Roller
# ============================================================

import random

DICE_ART = {
    1: ("┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"),
    2: ("┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"),
    3: ("┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"),
    4: ("┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"),
    5: ("┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"),
    6: ("┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘"),
}

def roll_dice(num_dice=1, sides=6):
    return [random.randint(1, sides) for _ in range(num_dice)]

def display_dice(values):
    if all(v <= 6 for v in values):
        rows = [[] for _ in range(5)]
        for val in values:
            art = DICE_ART[val]
            for i, line in enumerate(art):
                rows[i].append(line)
        for row in rows:
            print("  ".join(row))
    else:
        for v in values:
            print(f"  [ {v} ]", end="  ")
        print()

def dice_roller():
    print("=" * 45)
    print("           🎲 DICE ROLLER 🎲")
    print("=" * 45)
    print("Type 'quit' to exit\n")

    while True:
        try:
            num = input("How many dice to roll? (1-6): ").strip()
            if num.lower() == 'quit': break
            num = int(num)
            if not 1 <= num <= 6:
                print("Please enter a number between 1 and 6.\n")
                continue

            sides_input = input("How many sides? (default=6): ").strip()
            if sides_input.lower() == 'quit': break
            sides = int(sides_input) if sides_input else 6
            if sides < 2:
                print("Dice must have at least 2 sides.\n")
                continue

            results = roll_dice(num, sides)
            print(f"\nRolling {num} d{sides}...\n")
            display_dice(results)
            print(f"\nResults: {results}")
            print(f"Total: {sum(results)}")
            if num > 1:
                print(f"Average: {sum(results)/num:.1f}")
            print("-" * 45 + "\n")

        except ValueError:
            print("Invalid input!\n")

if __name__ == "__main__":
    dice_roller()
