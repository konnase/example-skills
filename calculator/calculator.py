import sys


def add(a: float, b: float) -> float:
    """Adds two numbers together."""
    return a + b


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python calculator.py <a> <b>")
        sys.exit(1)

    try:
        num1 = float(sys.argv[1])
        num2 = float(sys.argv[2])
        result = add(num1, num2)
        print(result)
    except ValueError:
        print("Error: Arguments must be numbers.")
        sys.exit(1)
