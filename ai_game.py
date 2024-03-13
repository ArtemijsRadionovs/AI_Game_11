import random

# Value array generation

def generate_array(len):
    value_array = {}
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

    
    return value_array

# Player's score printing
def print_players_score(A_score, B_score):
    print("Player's A score: " + str(A_score))
    print("Player's B score: " + str(B_score))

# Player's score depending on the choise


def turn_action(A_or_B_turn, arr, score):
    A = score["A"]
    B = score["B"]

    if len(arr) > 0:
        print("\n"+ A_or_B_turn +" turn:" +"\n")
        keys = str(arr.keys())
        while True:
            x = int(input("Enter one of these numbers " + keys[10:-1] + ": "))
            if x not in arr.keys():
                x = int(input("Enter one of these numbers " + keys[10:-1] + ": "))
            else:
                break
        arr_val = arr[x]
        match arr_val:
            case 1:
                print("\nYou have choose: 1\n")
                if A_or_B_turn == "A":
                    A -= 1
                else:
                    B -= 1
                print_players_score(A,B)
            case 2:
                print("\nYou have choose: 2\n")
                A -= 1
                B -= 1
                print_players_score(A,B)
            case 3:
                print("\nYou have choose: 3\n")
                if A_or_B_turn == "A":
                    B -= 1
                else:
                    A -= 1
                print_players_score(A,B)
        arr.pop(x)

        arr_values = str(arr.values())
        print("\n You have number numbers: " + arr_values[12:-1])
        
    score["A"] = A
    score["B"] = B
    return score

# Array length entering
def enter_val_arr_len():
    while True:
        # n = 5
        # return n
        n = int(input("Enter number from 15 to 25 how many values do you want in array: "))
        if n < 15 or n > 25:
            n = input("Enter number from 15 to 25 how many values do you want in array: ")
        else:
            return n

def analize_win(score):
    A = score["A"]
    B = score["B"]
    if A > B:
        print("Player A is a winner! Congratulations!")
    elif A < B:
        print("Player B is a winner! Congratulations!")
    else:
        print("It's a DRAW! Good game players!")

# Main part:
def main():
    n = enter_val_arr_len()
    value_array = generate_array(n)
    val_arr_copy = value_array.copy()
    val_arr_values = str(value_array.values())
    print("\n Array with numbers: " + val_arr_values[12:-1])

    A_B_scores = {"A":50,"B":50}
    for i in range(len(value_array)):
        A_B_scores = turn_action("A",val_arr_copy, A_B_scores)
        A_B_scores = turn_action("B",val_arr_copy, A_B_scores)
    analize_win(A_B_scores)

    
if __name__ == "__main__":
    main()
