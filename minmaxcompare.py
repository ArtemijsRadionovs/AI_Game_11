from typing import List, Tuple
from random import randint
import time

#include minmax.py
from minmax import turn_action, terminal_test, utility, minmax_decision, minmax_decision_ab, generate_array

# score - list of player's count state
def print_players_score(score: List[int]) -> None:
    print("Player 1 score: " + str(score[0]))
    print("Player 2 score: " + str(score[1]))

# Main function with calculation of time elapsed for minmax_decision function compared to minmax_decision_ab function
def main():
    # Initialize game state
    # input size of the array
    size = int(input("Enter size of the array: "))
    arr = generate_array(size)
    score = [50, 50]
    # Initialize variables
    # inicialize function with minmax_decision
    function = minmax_decision

    # input type of algorithm
    print("Choose algorithm:")
    print("1 - MinMax")
    print("2 - MinMax with alpha-beta pruning")
    algorithm = int(input())
    if algorithm == 1:
        function = minmax_decision
    elif algorithm == 2:
        function = minmax_decision_ab
    else:
        print("Invalid choice!")
        return

    player = 0
    # Main game loop
    while not terminal_test(arr):
        print("\nPlayer " + str(player + 1) + " turn:")
        print("Game board: " + str(arr))
        print_players_score(score)
        # save current time
        start_time = time.time()
        choice = function(arr, score, player)
        # print time elapsed
        print("Time elapsed: " + str(time.time() - start_time))
        score, arr = turn_action(player, arr, score, choice)
        player = 1 - player
    print("\nGame over!")
    print_players_score(score)
    if utility(score) == -1:
        print("Player 1 wins!")
    elif utility(score) == 1:
        print("Player 2 wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()