#This is a comment

name = "Seth" #name is a variable, "Seth" is a string, don't have to use semicolons at the end of python instructions.
last = 'LaFountain'
age = 35 #this is an integer, not a string
weight = 180.5 #this is a float
happy = True #this is a boolean value, must use capital
something = []

print("Hello World!") #this function is to show a value in the terminal, equivalent to console.log
print(age+1)
# print(name+1) #this will not work, you can only concatenate a string to another string.
print(name+" "+last)
print(f"{name} {last}") #adding the f is for a format string, just like using `` in javascript

def say_hello():
    print("Hi!!") #in python we will not use {} to contain the content of the function, but we will use an indent instead.
    print("This is inside the function")

say_hello()