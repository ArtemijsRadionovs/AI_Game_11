# Structure for MinMax algorithm for 2 players game with 3 possible choices: -1 0 1
# Inicial state is list of numbers from 1 to 3 and players count state 50 for each player
# Successor function is removing one number from the list and decreasing player's count state by 1 depending on the number: 1 - decrease player 1 count state, 2 - decrease both player's count state, 3 - decrease player 2 count state
# Terminal test is when the list is empty
# Utility function is returning -1 if player 1 wins, 1 if player 2 wins and 0 if it's a draw
# First player stored as 0, second player stored as 1
# MinMax algorithm is implemented without alpha-beta pruning

from typing import List, Tuple
from random import randint
import time

# Function game state return after player's turn. 
# player_turn - 0 for player 1, 1 for player 2
# arr - list of numbers from 1 to 3
# score - list of player's count state
# choice - player's choice index from 0 to len(arr) - 1
# return - updated player's count state and list of numbers
def turn_action(player_turn: int, arr: List[int], score: List[int], choice: int) -> Tuple[List[int], List[int]]:
    # check if the list of numbers (game board) is not empty
    if len(arr) > 0:
        # check if the player's choice is valid
        if choice < 0 or choice >= len(arr):
            return score, arr
        # get the chosen number from the list and remove it
        arr_val = arr.pop(choice)
        # decrease player's count state depending on the chosen number
        if arr_val == 1:
            if player_turn == 0:
                score[0] -= 1
            else:
                score[1] -= 1
        elif arr_val == 2:
            score[0] -= 1
            score[1] -= 1
        elif arr_val == 3:
            if player_turn == 0:
                score[1] -= 1
            else:
                score[0] -= 1
        return score, arr
    return score, arr

# Function for checking if the game is over
# arr - list of numbers from 1 to 3
# return - True if the list is empty, False otherwise
def terminal_test(arr: List[int]) -> bool:
    return len(arr) == 0

# Function for calculating the utility of the game
# score - list of player's count state
# where score[0] is player 1 count state and score[1] is player 2 count state
# return - -1 if player 1 wins, 1 if player 2 wins and 0 if it's a draw
def utility(score: List[int]) -> int:
    if score[0] > score[1]:
        return -1
    elif score[0] < score[1]:
        return 1
    else:
        return 0

# Function for MinMax algorithm
# arr - list of numbers from 1 to 3
# score - list of player's count state
# player - 0 for player 1, 1 for player 2
def minmax_decision(arr: List[int], score: List[int], player: int) -> int:
    def max_value(arr: List[int], score: List[int], player: int) -> int:
        if terminal_test(arr):
            return utility(score)
        v = float('-inf')
        for a in range(len(arr)):
            new_score, new_arr = turn_action(player, arr.copy(), score.copy(), a)
            v = max(v, min_value(new_arr, new_score, 1 - player))
        return v

    def min_value(arr: List[int], score: List[int], player: int) -> int:
        if terminal_test(arr):
            return utility(score)
        v = float('inf')
        for a in range(len(arr)):
            new_score, new_arr = turn_action(player, arr.copy(), score.copy(), a)
            v = min(v, max_value(new_arr, new_score, 1 - player))
        return v

    best_score = float('-inf')
    best_action = -1
    for a in range(len(arr)):
        new_score, new_arr = turn_action(player, arr.copy(), score.copy(), a)
        v = min_value(new_arr, new_score, 1 - player)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

# Function for MinMax algorithm with alpha-beta pruning
# arr - list of numbers from 1 to 3
# score - list of player's count state
# player - 0 for player 1, 1 for player 2
def minmax_decision_ab(arr: List[int], score: List[int], player: int) -> int:
    def max_value(arr: List[int], score: List[int], player: int, alpha: int, beta: int) -> int:
        if terminal_test(arr):
            return utility(score)
        v = float('-inf')
        for a in range(len(arr)):
            new_score, new_arr = turn_action(player, arr.copy(), score.copy(), a)
            v = max(v, min_value(new_arr, new_score, 1 - player, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(arr: List[int], score: List[int], player: int, alpha: int, beta: int) -> int:
        if terminal_test(arr):
            return utility(score)
        v = float('inf')
        for a in range(len(arr)):
            new_score, new_arr = turn_action(player, arr.copy(), score.copy(), a)
            v = min(v, max_value(new_arr, new_score, 1 - player, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_score = float('-inf')
    best_action = -1
    alpha = float('-inf')
    beta = float('inf')
    for a in range(len(arr)):
        new_score, new_arr = turn_action(player, arr.copy(), score.copy(), a)
        v = min_value(new_arr, new_score, 1 - player, alpha, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

# Function for generating array of numbers from 1 to 3
def generate_array(length: int) -> List[int]:
    value_array = []
    for i in range(length):
        value = randint(1, 3)
        value_array.append(value)
    return value_array