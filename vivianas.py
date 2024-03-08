import random

def generate_sequence(length):
    return [random.randint(1, 3) for _ in range(length)]

def play_game(sequence):
    player1_score = 50
    player2_score = 50

    for num in sequence:
        print("Virkne:", sequence)
        print("Spēlētāja 1 punkti:", player1_score)
        print("Spēlētāja 2 punkti:", player2_score)

        current_player = 1
        while True:
            print("Nākamais gājiens:", "Spēlētājs 1" if current_player == 1 else "Spēlētājs 2")
            choice = int(input("Izvēlieties ciparu ko noņemt (1-3): "))

            if choice < 1 or choice > 3:
                print("Jūs izvēlaties nepareizo ciparu.5 Jāizvēlas cipars no 1 - 3!")
            elif choice in sequence:
                sequence.remove(choice)

                if choice == 1:
                    if current_player == 1:
                        player1_score -= 1
                    else:
                        player2_score -= 1
                elif choice == 2:
                    player1_score -= 1
                    player2_score -= 1
                elif choice == 3:
                    if current_player == 1:
                        player2_score -= 1
                    else:
                        player1_score -= 1

                break
            else:
                print("Cipars neatrodas virknē. Jāizvēlas cits cipars.")

            current_player = 1 if current_player == 2 else 2

    print("Spēle beidzās!")
    print("Spēlētāja 1 punkti:", player1_score)
    print("Spēlētāja 2 punkti:", player2_score)

    if player1_score == player2_score:
        print("Tas ir neizšķirts!")
    elif player1_score > player2_score:
        print("Spēlētājs 1 UZVAR!")
    else:
        print("Spēlētājs 2 UZVAR!")

def main():
    length = random.randint(15, 25)
    sequence = generate_sequence(length)
    play_game(sequence)

if __name__ == "__main__":
    main()
