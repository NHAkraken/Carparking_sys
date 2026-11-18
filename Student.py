def add(x: float, y: float) -> float:
    return x + y

def subtract(x: float, y: float) -> float:
    return x - y

def multiply(x: float, y: float) -> float:
    return x * y

def divide(x: float, y: float) -> float:
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

def calculator():
    operations = {
        "1": ("+", add),
        "2": ("-", subtract),
        "3": ("*", multiply),
        "4": ("/", divide),
    }

    while True:
        print("\n--- SIMPLE CALCULATOR ---")
        print("1. Add (+)")
        print("2. Subtract (-)")
        print("3. Multiply (*)")
        print("4. Divide (/)")
        print("5. Exit")

        choice = input("Select operation (1-5): ").strip()

        if choice == "5":
            print("Exiting calculator.")
            break

        if choice not in operations:
            print("[Error] Invalid choice. Please select 1 through 5.")
            continue

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            symbol, func = operations[choice]
            result = func(num1, num2)
            
            # Format cleanly (removes trailing .0 for whole numbers)
            formatted_result = int(result) if result.is_integer() else round(result, 4)
            print(f"Result: {num1} {symbol} {num2} = {formatted_result}")

        except ValueError as e:
            print(f"[Error] {e if 'zero' in str(e) else 'Please enter valid numbers.'}")

if __name__ == "__main__":
    calculator()