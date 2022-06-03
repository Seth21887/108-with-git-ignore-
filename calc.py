#Calc.py
#Extreme calculator
#Seth

def menu():
    print("="*30)
    print("Extreme Calc")
    print("by Seth")
    print("="*30)
    print("[1] Sum")
    print("[2] Subtract")
    print("[3] Multiply")
    print("[4] Divide")
    print("[q] Exit")

option = '' # the variable option needs to be defined prior to it being used in the while loop below it, everything goes top to bottom in python
while option !="q":
    menu()
    option = input('Please select an option: ') #the user input will be stored in the variable option
    # print('The selected option is ' + option) #this is just a way to test if your code is working, don't need this print besides that.

    #ask for the number 1
    num1 = float(input("Please enter first number: ")) #we have to use float to parse the data from being a string
    #ask for the number 2
    num2 = float(input("Please enter second number: "))

    # print(f"DEBUG: num1:{num1} num2: {num2}")

    result = 0
    if option =="1":
        result = num1+num2
        print(f"The result is: {result}")
    elif option=="2": #elif means else, if
        result = num1-num2
        print(f"The result is: {result}")
    elif option=="3":
        result = num1*num2
        print(f"The result is: {result}")
    elif option=="4":
        if num2 != 0:
            result = num1/num2
            print(f"The result is: {result}")
        else:
            print('We cannot divide by zero')
    input('Press enter to continue...')
