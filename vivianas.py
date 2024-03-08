import random

def generate_sequence(length):
    return [random.randint(1, 3) for _ in range(length)]

def play_game(sequence):
    player_score = 50
    opponent_score = 50

    for num in sequence:
        print("Tavs gājiens. Tava pašreizējā punktu skaits:", player_score)
        choice = int(input("Izvēlies, kādu punktu skaitli izņemt (1, 2 vai 3): "))
        if choice == 1:
            player_score -= 1
        elif choice == 2:
            player_score -= 1
            opponent_score -= 1
        elif choice == 3:
            opponent_score -= 1

        print("Pretinieka gājiens. Pretinieka pašreizējā punktu skaits:", opponent_score)
        print()

    if player_score == opponent_score:
        return "Neizšķirts!"
    elif player_score > opponent_score:
        return "Tu uzvarēji!"
    else:
        return "Tu zaudēji!"

def main():
    length = random.randint(15, 25)
    sequence = generate_sequence(length)
    result = play_game(sequence)
    print("Spēles virkne:", sequence)
    print("Rezultāts:", result)

if __name__ == "__main__":
    main()
