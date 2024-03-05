import random

# Value array generation
value_array = {}

def generate_array(len):
    for i in range(len):
        value = random.randint(1, 3)
        value_array.update({(i+1):value})

    # value_array = {
    #   1: 3,
    #   2: 2,
    #   3: 3,
    #   4: 1,
    #   5: 2
    # }

    value_array_copy = value_array.copy()
    return value_array_copy

# Player's score printing
def print_players_score(A_score, B_score):
    print("Player's A score: " + str(A_score))
    print("Player's B score: " + str(B_score))

# Player's score depending on the choise
A_B_scores = {"A":50,"B":50}

def turn_action(A_or_B_turn, arr, score):
    A = score["A"]
    B = score["B"]

    if len(arr) > 0:
        print("\n"+ A_or_B_turn +" turn:" +"\n")
        keys = str(arr.keys())
        x = int(input("Enter one of these numbers " + keys[10:-1] + ": "))
        arr_val = arr[x]
        match arr_val:
            case 1:
                print("\nYou have choose: 1")
                if A_or_B_turn == "A":
                    A -= 1
                else:
                    B -= 1
                print_players_score(A,B)
            case 2:
                print("\nYou have choose: 2")
                A -= 1
                B -= 1
                print_players_score(A,B)
            case 3:
                print("\nYou have choose: 3")
                if A_or_B_turn == "A":
                    B -= 1
                else:
                    A -= 1
                print_players_score(A,B)
        arr.pop(x)
        print()
        print(arr.values())
    score["A"] = A
    score["B"] = B
    return score

# Array length entering
def enter_val_arr_len():
    while True:
        # n = 10
        # return n
        n = int(input("Enter number from 15 to 25 how many values do you want in array: "))
        if n < 15 or n > 25:
            n = input("Enter number from 15 to 25 how many values do you want in array: ")
        else:
            return n

# Main part:
n = enter_val_arr_len()
val_arr_copy = generate_array(n)

print(value_array.values())

for i in range(len(value_array)):
    A_B_scores = turn_action("A",val_arr_copy, A_B_scores)
    A_B_scores = turn_action("B",val_arr_copy, A_B_scores)
