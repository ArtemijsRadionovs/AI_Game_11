import random

# class State:
#     def __init__(self, num_dict, A_B_score, lvl = 0):
#         self.num_dict = num_dict
#         self.A_B_score = A_B_score
#         self.rating = 0
#         self.level = lvl
#         # add depth

#     # Heiristiskā funkcija
#     def count_rating(self):
#         A_B_score = self.A_B_score
#         A_score = A_B_score["A"]
#         B_score = A_B_score["B"]
#         score_differ = A_score - B_score

#         num_dict = self.num_dict
#         one_count = 0
#         three_count = 0
#         for key in num_dict.keys():
#             value = num_dict[key]
#             if value == 1:
#                 one_count += 1
#             elif value == 3:
#                 three_count -= 1
        
#         self.rating = one_count + three_count + score_differ

# Value array generation

def generate_array(len):
    value_array = {}

    # Return from commenting:
    # for i in range(len):
    #     value = random.randint(1, 3)
    #     value_array.update({(i+1):value})
    #
    
    # Test array:
    value_array = {
      1: 3,
      2: 2,
      3: 3,
      4: 1,
      5: 2
    }
  
    return value_array

# Player's score printing
def print_players_score(A_score, B_score):
    print("Player's A score: " + str(A_score))
    print("Player's B score: " + str(B_score))

# Choose who will start
def choose_first():
    while True:
        first = input("Who will start Computer or Human? Enter Computer or Human: ")
        if first == "Computer":
            second = "Human"
            print("\nComputer is Player A now!")
            print("Human is Player B now!")
            return first, second
        elif first == "Human":
            second = "Computer"
            print("\nHuman is Player A now!")
            print("Computer is Player B now!")
            return first, second
        else:
            print("\nType Computer or Human!")

# Player's score depending on the choise
def turn_action(A_or_B_turn, arr, score):
    A = score["A"]
    B = score["B"]

    if len(arr) > 0:
        print("\n"+ A_or_B_turn +" turn:" +"\n")
        keys = str(arr.keys())
        while True:
            x = input("Enter one of these numbers " + keys[10:-1] + ": ")
            if x.isdigit():
                 x = int(x)
                 if x in arr.keys():
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
            case _:
                print("\nChoose a number!\n")
        arr.pop(x)

    if len(arr) > 0:
        arr_values = str(arr.values())
        print("\n You have number numbers: " + arr_values[12:-1])

    score["A"] = A
    score["B"] = B
    return score

# Array length entering
def enter_val_arr_len():
    while True:
        # Test length:
        n = 5
        return n
    
        # Return from commenting:
        # n = input("Enter number from 15 to 25 how many values do you want in array: ")
        # if n.isdigit():
        #     n = int(n)
        #     if 15 <= n <= 25:
        #         return n
        # print("Invalid input! Type a digit from 15 to 25.!")
        # 
    
def analize_win(score):
    A = score["A"]
    B = score["B"]
    if A > B:
        print("\nPlayer A is a winner! Congratulations!")
    elif A < B:
        print("\nPlayer B is a winner! Congratulations!")
    else:
        print("\nIt's a DRAW! Good game players!")

# Main part:
def main():
    n = enter_val_arr_len()
    value_array = generate_array(n)
    val_arr_copy = value_array.copy()
    val_arr_values = str(value_array.values())
    print("\n Array with numbers: " + val_arr_values[12:-1])

    A_B_scores = {"A":50,"B":50}

    # new part start
    first, second = choose_first()
    

    for _ in value_array:
        A_B_scores = turn_action(first,val_arr_copy, A_B_scores)
        A_B_scores = turn_action(second,val_arr_copy, A_B_scores)
    # new part end
        
    analize_win(A_B_scores)
    
if __name__ == "__main__":
    main()