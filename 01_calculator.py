# ============================================================
# PROJECT 1: Calculator
# ============================================================

def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        return "Error: Division by zero!"
    return a / b

def calculator():
    print("=" * 40)
    print("         PYTHON CALCULATOR")
    print("=" * 40)
    print("Operations: +  -  *  /")
    print("Type 'quit' to exit\n")

    while True:
        try:
            num1 = input("Enter first number: ")
            if num1.lower() == 'quit': break
            num1 = float(num1)

            op = input("Enter operator (+, -, *, /): ").strip()
            if op not in ['+', '-', '*', '/']:
                print("Invalid operator!\n")
                continue

            num2 = input("Enter second number: ")
            if num2.lower() == 'quit': break
            num2 = float(num2)

            if op == '+':   result = add(num1, num2)
            elif op == '-': result = subtract(num1, num2)
            elif op == '*': result = multiply(num1, num2)
            elif op == '/': result = divide(num1, num2)

            print(f"\nResult: {num1} {op} {num2} = {result}\n")
            print("-" * 40)

        except ValueError:
            print("Invalid input! Please enter numbers.\n")

if __name__ == "__main__":
    calculator()
