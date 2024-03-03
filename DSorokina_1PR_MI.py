def main():
  print("Welcome to the game!")
  first_player = choose_first_player()
  length = get_length()
  numbers = generate_numbers(length)
  player_scores = [50, 50]

  current_player_num = first_player

  while len(numbers)>0:
      print(f"\nCurrent string of numbers: {numbers}")
      print(f"Player 1: {player_scores[0]} points")
      print(f"Player 2: {player_scores[1]} points")
      print(f"Player's {current_player_num} turn: ")
      choice = get_choice(numbers)
      remove_num(numbers, choice, player_scores, current_player_num)
      current_player_num = 1 if current_player_num == 2 else 2 
   

  print("\nGame over!")
  print_score(player_scores)    



def choose_first_player():
  while True:
    try:
      first_player = int(input("Chose first player (1 or 2): "))
      if first_player in [1,2]:
        return first_player
      else:
        print("Invalid choise")
    except ValueError:
      print("Enter an integer (1 or 2)")
                               

def get_length():
  while True:
      try:
          length = int(input("Enter the length of the string(from 15 to 25): "))
          if 15 <= length <= 25:
              return length
          else:
              print("The length should be in the range from 15 to 25.")
      except ValueError:
          print("Enter and integer.")

def generate_numbers(length):
  import random;
  return[random.randint(1,3) for _ in range(length)]

def current_player(numbers_left):
  return 1 if numbers_left % 2 == 0 else 2

def get_choice(numbers):
  while True:
      try:
          choice = int(input("Select the number to delete(1, 2 or 3): "))
          if choice in [1,2,3] and choice in numbers:
              return choice
          else:
              print("Invalid selection")
      except ValueError:
          print("Enter an integer (1, 2 or 3)")

def remove_num(numbers, choice, player_scores, current_player_num):
  numbers.remove(choice)
  if choice == 1:
      player_scores[current_player_num-1] -= 1
  elif choice == 3:
      player_scores[2-current_player_num] -= 1
  else:
      player_scores[0] -= 1
      player_scores[1] -= 1

def print_score(player_scores):
  print(f"Player 1: {player_scores[0]} points")
  print(f"Player 2: {player_scores[1]} points")
  if player_scores[0] == player_scores[1]:
      print("Draw!")
  else:
      winner = 1 if player_scores[0] > player_scores[1] else 2
      print(f"Player {winner} wins!")


if __name__ == "__main__":
  main()