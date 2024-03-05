import random

def generate_numbers(length):
    # Ģenerē skaitļu virkni ar norādīto garumu, katrs skaitlis ir no 1 līdz 3.
    return [random.randint(1, 3) for _ in range(length)]

def play_game(numbers):
    # Inicializē spēlētāju un pretinieka punktu skaitu.
    player_score = 50
    opponent_score = 50

    # Veic spēli, izmantojot katru skaitli no ģenerētās skaitļu virknes.
    for number in numbers:
        if number == 1:
            player_score -= 1
        elif number == 2:
            player_score -= 1
            opponent_score -= 1
        elif number == 3:
            opponent_score -= 1

    # Atgriež abu spēlētāju punktu skaitu pēc spēles beigām.
    return player_score, opponent_score

def main():
    # Ievada skaitļu virknes garumu no 15 līdz 25.
    length = int(input("Ievadiet skaitļu virknes garumu (no 15 līdz 25): "))
    # Pārbauda, vai ievadītais garums atbilst prasībām.
    while length < 15 or length > 25:
        print("Skaitļu virknes garums jābūt no 15 līdz 25.")
        length = int(input("Lūdzu, ievadiet derīgu garumu: "))

    # Ģenerē skaitļu virkni ar norādīto garumu.
    numbers = generate_numbers(length)
    print("Ģenerētā skaitļu virkne:", numbers)

    # Izpilda spēli, izmantojot ģenerēto skaitļu virkni.
    player_score, opponent_score = play_game(numbers)

    # Izvada rezultātu, kurš uzvarēja vai vai spēle beidzās neizšķirti.
    if player_score == opponent_score:
        print("Spēle beidzās neizšķirti! Abiem spēlētājiem ir vienāds punktu skaits:", player_score)
    elif player_score > opponent_score:
        print("Spēlētājs uzvar ar punktu skaitu:", player_score)
    else:
        print("Pretinieks uzvar ar punktu skaitu:", opponent_score)

if __name__ == "__main__":
    main()