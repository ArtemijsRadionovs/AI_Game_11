import random

def generate_sequence(length):
    return [random.randint(1, 3) for _ in range(length)]

def play_game(sequence):
    player1_points = 50
    player2_points = 50
    current_player = 1

    while sequence:
        print("Virkne:", sequence)
        print("Spēlētāja 1 punkti:", player1_points)
        print("Spēlētāja 2 punkti:", player2_points)
        print("Nākamais gājiens:", "Spēlētājs 1" if current_player == 1 else "Spēlētājs 2")

        choice = int(input("Izvēlieties ciparu ko noņemt (1-3): "))

        if choice < 1 or choice > 3:
            print("Nekā! Jāizvēlas cipars no 1 - 3!")
            continue

        if choice in sequence:
            sequence.remove(choice)

            if choice == 1:
                if current_player == 1:
                    player1_points -= 1
                else:
                    player2_points -= 1
            elif choice == 2:
                player1_points -= 1
                player2_points -= 1
            elif choice == 3:
                if current_player == 1:
                    player2_points -= 1
                else:
                    player1_points -= 1

            current_player = 1 if current_player == 2 else 2
        else:
            print("Cipars neatrodas virknē. Jāizvēlas cits cipars.")
            continue

    print("Spēles beigas!")
    print("SPēlētāja 1 punkti:", player1_points)
    print("Spēlētāja 2 punkti:", player2_points)

    if player1_points == player2_points:
        print("Tas ir neizšķirts!")
    elif player1_points > player2_points:
        print("Spēlētājs 1 UZVAR!")
    else:
        print("Spēlētājs 2 UZVAR!")

def main():
    length = int(input("Ievadiet virknes garumu (15-25): "))
    sequence = generate_sequence(length)
    play_game(sequence)

if __name__ == "__main__":
    main()
