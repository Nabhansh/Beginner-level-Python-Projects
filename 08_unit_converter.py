# ============================================================
# PROJECT 8: Unit Converter
# ============================================================

CONVERSIONS = {
    "Length": {
        "units": ["Meters", "Kilometers", "Centimeters", "Millimeters",
                   "Miles", "Yards", "Feet", "Inches"],
        "to_base": {   # base = meters
            "Meters": 1, "Kilometers": 1000, "Centimeters": 0.01,
            "Millimeters": 0.001, "Miles": 1609.344, "Yards": 0.9144,
            "Feet": 0.3048, "Inches": 0.0254
        }
    },
    "Weight": {
        "units": ["Kilograms", "Grams", "Milligrams", "Pounds", "Ounces", "Tonnes"],
        "to_base": {   # base = kilograms
            "Kilograms": 1, "Grams": 0.001, "Milligrams": 0.000001,
            "Pounds": 0.453592, "Ounces": 0.0283495, "Tonnes": 1000
        }
    },
    "Temperature": {
        "units": ["Celsius", "Fahrenheit", "Kelvin"],
        "special": True
    },
    "Area": {
        "units": ["Square Meters", "Square Kilometers", "Square Feet",
                   "Square Miles", "Hectares", "Acres"],
        "to_base": {   # base = square meters
            "Square Meters": 1, "Square Kilometers": 1e6,
            "Square Feet": 0.092903, "Square Miles": 2.59e6,
            "Hectares": 10000, "Acres": 4046.86
        }
    },
    "Speed": {
        "units": ["m/s", "km/h", "mph", "knots", "ft/s"],
        "to_base": {   # base = m/s
            "m/s": 1, "km/h": 0.277778, "mph": 0.44704,
            "knots": 0.514444, "ft/s": 0.3048
        }
    },
    "Volume": {
        "units": ["Liters", "Milliliters", "Gallons (US)", "Quarts", "Pints", "Cups", "Fluid Ounces"],
        "to_base": {   # base = liters
            "Liters": 1, "Milliliters": 0.001, "Gallons (US)": 3.78541,
            "Quarts": 0.946353, "Pints": 0.473176, "Cups": 0.24,
            "Fluid Ounces": 0.0295735
        }
    },
    "Time": {
        "units": ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"],
        "to_base": {   # base = seconds
            "Seconds": 1, "Minutes": 60, "Hours": 3600, "Days": 86400,
            "Weeks": 604800, "Months": 2628000, "Years": 31536000
        }
    }
}

def convert_temperature(value, from_unit, to_unit):
    # Convert to Celsius first
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        celsius = value

    # Convert from Celsius to target
    if to_unit == "Fahrenheit":
        return celsius * 9/5 + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    else:
        return celsius

def convert_units(value, from_unit, to_unit, category):
    if category == "Temperature":
        return convert_temperature(value, from_unit, to_unit)
    to_base = CONVERSIONS[category]["to_base"]
    base_value = value * to_base[from_unit]
    return base_value / to_base[to_unit]

def select_from_list(items, prompt):
    for i, item in enumerate(items, 1):
        print(f"  {i:2}. {item}")
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(items):
                return items[choice - 1]
            print(f"Please enter 1-{len(items)}")
        except ValueError:
            print("Invalid input!")

def main():
    print("=" * 50)
    print("         🔄 UNIT CONVERTER")
    print("=" * 50)

    while True:
        print("\nCategories:")
        categories = list(CONVERSIONS.keys())
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")
        print(f"  {len(categories)+1}. Quit")

        try:
            cat_choice = int(input(f"\nSelect category (1-{len(categories)+1}): "))
        except ValueError:
            continue

        if cat_choice == len(categories) + 1:
            print("\nGoodbye! 👋")
            break
        if not 1 <= cat_choice <= len(categories):
            print("Invalid choice!")
            continue

        category = categories[cat_choice - 1]
        units = CONVERSIONS[category]["units"]

        print(f"\n{category} Units:")
        from_unit = select_from_list(units, "Convert FROM (number): ")

        print(f"\nConvert TO:")
        to_unit = select_from_list(units, "Convert TO (number): ")

        try:
            value = float(input(f"\nEnter value in {from_unit}: "))
        except ValueError:
            print("Invalid number!")
            continue

        result = convert_units(value, from_unit, to_unit, category)

        print(f"\n{'='*50}")
        print(f"  {value:,.4f} {from_unit}")
        print(f"  = {result:,.6f} {to_unit}")
        print(f"{'='*50}")

        # Show common conversions
        if input("\nSee all conversions from this value? (y/n): ").lower() == 'y':
            print(f"\n  {value} {from_unit} =")
            for unit in units:
                if unit != from_unit:
                    r = convert_units(value, from_unit, unit, category)
                    print(f"    {r:>15,.4f} {unit}")

if __name__ == "__main__":
    main()
