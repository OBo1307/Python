num = int(input("Enter a number to be divided: "))
start = int(input("Enter a starting pint for the divisor: "))
end = int(input("Enter an end point for the divisor: "))

for div in range(start, end):
    if div == 0:
        print("Division by zero, exiting.")
        continue
    print(num / div)



                