# #range(5) -----> [0, 1, 2, 3, 4] will return a 5 element array.
# n = input('How many times do you want to repeat the message?') #this value will output a string, so it should be converted to an integer, either here or in the loop

# for i in range(int(n)):
#     # i = 0, i = 1, etc.
#     print(f"Hello World {i}" ) #Show i here

elements = ["a", "b", "c", "a"] #in lists, we can repreat values

#range(4) ----> [0,1,2,3] range returns integers, instead of using range, we can use the name of the actual list, and print it that way.
print("Slower Form")
for i in range(4):
    print(elements[i])

print("Cooler Form")
for e in elements:
    print(e)

#this is a dictionary, all keys must be strings, values can be any type of data: str, int, float, object
#cannot have repeated keys, not the same as a list.
me = {
    "first": "Seth",
    "last": "LaFountain",
    "age": 35
}

print( me["first"] )