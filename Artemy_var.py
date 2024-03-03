import random

A = 50
B = 50

# n = input("Enter how many values do you want in array: ")
n = 10
value_array = {}

for i in range(n):
    value = random.randint(1, 3)
    value_array.update({(i+1):value})




# value_array = {
#   1: 3,
#   2: 2,
#   3: 3,
#   4: 1,
#   5: 2,
#   6: 3,
#   7: 2,
#   8: 1,
#   9: 3,
#   10: 2
# }

value_array_copy = value_array.copy()

print(value_array.values())
print()

for i in range(len(value_array)):
    if len(value_array_copy) > 0:
        print("A turn:")
        keys = str(value_array_copy.keys())
        x = int(input("Enter one of these numbers " + keys[10:41] + ": "))
        print()
        arr_val = value_array_copy[x]
        if arr_val == 1:
            print("You have choose: 1")
            A -= 1
            print("Player's A score: " + str(A))
            print("Player's B score: " + str(B))
        if arr_val == 2:
            print("You have choose: 2")
            A -= 1
            B -= 1
            print("Player's A score: " + str(A))
            print("Player's B score: " + str(B))
        if arr_val == 3:
            print("You have choose: 3")
            B -= 1
            print("Player's A score: " + str(A))
            print("Player's B score: " + str(B))
        value_array_copy.pop(x)
        print()
        print(value_array_copy.values())
        
    if len(value_array_copy) > 0:
        print()
        print("B turn:")
        keys = str(value_array_copy.keys())
        y = int(input("Enter one of these numbers " + keys[10:41] + ": "))
        print()
        arr_val = value_array_copy[y]
        if arr_val == 1:
            print("You have choose: 1")
            A -= 1
            print("Player's A score: " + str(A))
            print("Player's B score: " + str(B))
        if arr_val == 2:
            print("You have choose: 2")
            A -= 1
            B -= 1
            print("Player's A score: " + str(A))
            print("Player's B score: " + str(B))
        if arr_val == 3:
            print("You have choose: 3")
            B -= 1
            print("Player's A score: " + str(A))
            print("Player's B score: " + str(B))
        value_array_copy.pop(y)
        print()
        print(value_array_copy.values())
