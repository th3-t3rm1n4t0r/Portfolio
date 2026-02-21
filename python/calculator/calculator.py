def main():
    print("Calculator")

    print("+ for Addition")
    print("- for Subtraction")
    print("* for Multiplication")
    print("/ for Division")
    print("** for Exponentiation")
    print("// for Floor Division")
    print("Press Ctrl-D to exit")

    num1 = float(input("Enter a number: "))
    oper = operation()
    num2 = float(input("Enter another number: "))

    

def operation():
    oper_list = ["+", "-", "*", "/", "**", "//"]
    while True:
        try:
            oper = input("Enter an operator: ")
            assert oper in oper_list
        except EOFError:
            break
        except AssertionError:
            print("Enter a valid operator.")
        except ValueError:
            print("Enter a floating point number or an integer.")
        else:            
            return oper

def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 == 0:
        raise ZeroDivisionError
    else:
        return round(num1 / num2, 2)
    
def fdivide(num1, num2):
    if num2 == 0:
        raise ZeroDivisionError
    else:
        return (num1 // num2)
    
def exponent(num1, num2):
    return num1 ** num2

if __name__ == "__main__":
    main()