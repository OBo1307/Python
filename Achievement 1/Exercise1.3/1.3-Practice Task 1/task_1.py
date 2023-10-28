number1 = float(input("Enter first number: "))
number2 = float(input("Enter second number: "))
operation = input("Enter the operator (+, -): ")

if operation == "+":
    result = number1 + number2
    print("The sum of the two numbers is:", result)
elif operation == "-":
    result = number1 - number2
    print("The difference of the two numbers is:", result)
else:
    print("Invalid operator")