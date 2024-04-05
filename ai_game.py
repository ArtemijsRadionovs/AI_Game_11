import pygame
import sys
import random
from tree_logic import selectMinMax, selectAlphaBeta, growBranch, getInd, nodes

# Static color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_YELLOW = (255, 215, 0)

# Define Player class
class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

# Function to generate array
def generate_array(length):
    value_array = {}

    for i in range(length):
        value = random.randint(1, 3)
        value_array.update({(i+1):value})
    
    return value_array

# Function to print players' scores
def print_players_score(screen, players):
    font = pygame.font.SysFont(None, 24)
    for i, player in enumerate(players):
        text = font.render(f"{player.name} score: {player.score}", True, BLACK)
        screen.blit(text, (20, 20 + i * 30))


# Function to display whose turn it is
def display_turn(screen, current_player):
    font = pygame.font.SysFont(None, 24)
    if current_player.name == "Player":
        text = font.render("Turn: Player", True, BLACK)
    else:
        text = font.render("Turn: Computer", True, BLACK)
    text_rect = text.get_rect(topright=(screen.get_width() - 20, 20))
    screen.blit(text, text_rect)


# Function for player's turn
def turn_action(current_player, arr, players):
    if len(arr) > 0:
        print(f"\n{current_player.name} turn:\n")
        keys = str(arr.keys())
        while True:
            x = input(f"Enter one of these numbers {keys[10:-1]}: ")
            if x.isdigit():
                x = int(x)
                if x in arr.keys():
                    break
        arr_val = arr[x]
        if arr_val == 1:
            print("\nYou have chosen: 1\n")
            current_player.score -= 1
        elif arr_val == 2:
            print("\nYou have chosen: 2\n")
            for player in players:
                player.score -= 1
        elif arr_val == 3:
            print("\nYou have chosen: 3\n")
            players[1 - players.index(current_player)].score -= 1
        else:
            print("\nChoose a number!\n")
        arr.pop(x)
    return players


# Function to display input box for array length
def enter_val_arr_len(screen):
    input_text = ""
    error_message = ""
    font = pygame.font.SysFont(None, 36)
    text = font.render("Enter Array Length (15-25):", True, BLACK)
    text_rect = text.get_rect(center=screen.get_rect().center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        n = int(input_text)
                        if 15 <= n <= 25:
                            return n
                        else:
                            error_message = "Wrong value! Enter a number between 15 and 25."
                    except ValueError:
                        error_message = "Not a number! Enter a number between 15 and 25."
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    error_message = ""
                else:
                    input_text += event.unicode

        screen.fill(WHITE)
        screen.blit(text, text_rect)
        font = pygame.font.SysFont(None, 48)
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (text_rect.centerx - input_surface.get_width() // 2, text_rect.centery + 50))

        
        # Display error message
        if error_message:
            error_font = pygame.font.SysFont(None, 35)
            error_text = error_font.render(error_message, True, RED)
            error_text_rect = error_text.get_rect(center=(text_rect.centerx, text_rect.centery + 100))
            screen.blit(error_text, error_text_rect)
        
        pygame.display.flip()
            
            
# Function to analyze win and return winner's name
def analyze_win(players):
    if players[0].score > players[1].score:
        return players[0].name
    elif players[0].score < players[1].score:
        return players[1].name
    else:
        return "Draw"

# Function to choose starter
def choose_starter(screen):
    starter_choice = None
    starter_choice_screen = pygame.Surface(screen.get_size())
    starter_choice_screen.fill(WHITE)
    font = pygame.font.SysFont(None, 36)
    text_starter_choice = font.render("Who will start?", True, BLACK)
    text_rect_starter_choice = text_starter_choice.get_rect(center=starter_choice_screen.get_rect().center)
    text_rect_starter_choice.y -= 50
    starter_choice_screen.blit(text_starter_choice, text_rect_starter_choice)

    button_font = pygame.font.SysFont(None, 30)
    button_width = 145
    button_height = 50
    button_margin = 10

    # Calculate the total height of the buttons and the text
    total_height = button_height * 2 + button_margin

    # Calculate the starting y position for the buttons and text
    start_y = (starter_choice_screen.get_height() - total_height) // 2

    button_x = (screen.get_width() - button_width) // 2

    # Adjust the position of the text and buttons
    text_rect_starter_choice.y = start_y

    # Button "Player"
    button_y_player = start_y + text_rect_starter_choice.height + button_margin
    text_player_button = button_font.render("Player", True, WHITE)
    text_rect_player_button = text_player_button.get_rect(center=(button_x + button_width // 2, button_y_player + button_height // 2))
    pygame.draw.rect(starter_choice_screen, RED, (button_x, button_y_player, button_width, button_height))
    starter_choice_screen.blit(text_player_button, text_rect_player_button)

    # Button "Computer"
    button_y_computer = button_y_player + button_height + button_margin
    text_computer_button = button_font.render("Computer", True, WHITE)
    text_rect_computer_button = text_computer_button.get_rect(center=(button_x + button_width // 2, button_y_computer + button_height // 2))
    pygame.draw.rect(starter_choice_screen, RED, (button_x, button_y_computer, button_width, button_height))
    starter_choice_screen.blit(text_computer_button, text_rect_computer_button)

    screen.blit(starter_choice_screen, (0, 0))
    pygame.display.flip()

    while not starter_choice:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if text_rect_player_button.collidepoint(mouse_pos):
                    starter_choice = "Player"
                elif text_rect_computer_button.collidepoint(mouse_pos):
                    starter_choice = "Computer"

    return starter_choice

# Function to choose algorithm
def choose_algorithm(screen):
    algorithm_choice = None
    algorithm_choice_screen = pygame.Surface(screen.get_size())
    algorithm_choice_screen.fill(WHITE)
    
    # Text "Choose algorithm:"
    font = pygame.font.SysFont(None, 36)
    text_algorithm_choice = font.render("Choose algorithm:", True, BLACK)
    text_rect_algorithm_choice = text_algorithm_choice.get_rect(center=algorithm_choice_screen.get_rect().center)
    text_rect_algorithm_choice.y -= 55
    algorithm_choice_screen.blit(text_algorithm_choice, text_rect_algorithm_choice)
    
    # Button "MinMax"
    button_font = pygame.font.SysFont(None, 30)
    button_width = 145
    button_height = 50
    button_margin = 20
    button_padding = 15  # Added padding between buttons

    button_x = (algorithm_choice_screen.get_width() - button_width) // 2
    button_y_minmax = text_rect_algorithm_choice.bottom + button_margin
    button_y_alphabeta = button_y_minmax + button_height + button_padding  # Adjusted position

    text_minmax_button = button_font.render("MinMax", True, WHITE)
    text_rect_minmax_button = text_minmax_button.get_rect(center=(button_x + button_width // 2, button_y_minmax + button_height // 2))

    # Button "Alpha-beta"
    text_alphabeta_button = button_font.render("Alpha-beta", True, WHITE)
    text_rect_alphabeta_button = text_alphabeta_button.get_rect(center=(button_x + button_width // 2, button_y_alphabeta + button_height // 2))

    # Blit text and buttons to the screen
    pygame.draw.rect(algorithm_choice_screen, RED, (button_x, button_y_minmax, button_width, button_height))
    algorithm_choice_screen.blit(text_minmax_button, text_rect_minmax_button)
    pygame.draw.rect(algorithm_choice_screen, RED, (button_x, button_y_alphabeta, button_width, button_height))  # Adjusted position
    algorithm_choice_screen.blit(text_alphabeta_button, text_rect_alphabeta_button)

    screen.blit(algorithm_choice_screen, (0, 0))
    pygame.display.flip()

    # Event handling
    while not algorithm_choice:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if text_rect_minmax_button.collidepoint(mouse_pos):
                    algorithm_choice = "MinMax"
                elif text_rect_alphabeta_button.collidepoint(mouse_pos):
                    algorithm_choice = "Alpha-beta"

    return algorithm_choice

# Function to draw squares with numbers
def draw_squares(screen, squares):
    font = pygame.font.SysFont(None, 50)
    square_rects = {}  # Dictionary to store square rectangles
    for i, (x, value) in enumerate(squares.items(), start=1):
        square_text = font.render(str(value), True, DARK_YELLOW)
        square_rect = square_text.get_rect(center=(x * 35, 120))
        pygame.draw.rect(screen, RED, square_rect)
        screen.blit(square_text, square_rect)
        square_rects[x] = square_rect  # Store rectangle in dictionary with square number as key
    return square_rects

def computer_use_algorithm(algorithm_choice, ind):
    # Chosen algorithm
    
    if algorithm_choice == "MinMax":
        # selectMinMax(ind, True)
        tree_elem, tree_ind, tree_rating = selectMinMax(ind, True)
        best_node_ind = nodes[tree_ind]['ind']
        print("Best node:", best_node_ind)
        square = nodes[best_node_ind]['elem']
        lvl = nodes[best_node_ind]['lvl']
        return square, lvl, best_node_ind
        
    elif algorithm_choice == "Alpha-beta":
        # selectAlphaBeta(ind, float('-inf'), float('inf'), True)
        tree_elem, tree_ind, tree_rating = selectAlphaBeta(ind, float('-inf'), float('inf'), True)
        best_node_ind = nodes[tree_ind]['ind']
        print("Best node:", best_node_ind)
        square = nodes[best_node_ind]['elem']
        lvl = nodes[best_node_ind]['lvl']
        return square, lvl, best_node_ind

    # Initialize the global variables


# Function to run the game
def run_game(screen):
    player1 = Player("Player", 50)
    player2 = Player("Computer", 50)
    players = [player1, player2]

    array_length = enter_val_arr_len(screen)
    game_array = generate_array(array_length)
    ind = 0
    ind = getInd()
    growBranch(ind, 0, game_array, player1.score, player2.score, 0)

    for i in nodes:
        print(nodes[i])
    
    starter_choice = choose_starter(screen)
    if starter_choice == "Computer":
        current_player = player2
    else:
        current_player = player1

    algorithm_choice = choose_algorithm(screen)
    print("Chosen algorithm:", algorithm_choice)
    # if algorithm_choice == "MinMax":
    #     selectMinMax(ind, True)
    # elif algorithm_choice == "Alpha-beta":
    #     selectAlphaBeta(ind, float('-inf'), float('inf'), True)
    square_rects = draw_squares(screen, game_array)

    running = True


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                ind = 0
                return 'No one' # Return 'quit' to exit the game

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for square, square_rect in square_rects.items():

                    if square_rect.collidepoint(mouse_pos):  # Check if mouse click occurred within the square button
                        if square in game_array:  # Check if the square number exists in the array
                            if current_player.name == "Player":
                                arr_val = game_array[square]
                                if arr_val == 1:
                                    print("\nYou have chosen: 1\n")
                                    current_player.score -= 1
                                elif arr_val == 2:
                                    print("\nYou have chosen: 2\n")
                                    for player in players:
                                        player.score -= 1
                                elif arr_val == 3:
                                    print("\nYou have chosen: 3\n")
                                    players[1 - players.index(current_player)].score -= 1
                                
                                game_array.pop(square)  # Remove the clicked square from the array
                                
                                element = nodes[ind]['elem']
                                if element == square:
                                    ind = nodes['ind']
                                growBranch(ind, square, game_array, player1.score, player2.score, 0)

                                current_player = players[1 - players.index(current_player)]  # Switch turn to the other player

                                if current_player.name == "Computer":
                                    if game_array:  # Check if the game array is not empty
                                        square, lvl, best_node_ind = computer_use_algorithm(algorithm_choice, ind)

                                        arr_val = game_array[square]
                                        if arr_val == 1:
                                            print("\nYou have chosen: 1\n")
                                            current_player.score -= 1
                                        elif arr_val == 2:
                                            print("\nYou have chosen: 2\n")
                                            for player in players:
                                                player.score -= 1
                                        elif arr_val == 3:
                                            print("\nYou have chosen: 3\n")
                                            players[1 - players.index(current_player)].score -= 1
                                        
                                        game_array.pop(square)  # Remove the clicked square from the array
                                        
                                        growBranch(best_node_ind, square, game_array, player1.score, player2.score, lvl)

                                        current_player = players[1 - players.index(current_player)]  # Switch turn to the other player
                            
                            elif current_player.name == "Computer":
                                square, lvl, best_node_ind = computer_use_algorithm(algorithm_choice, ind)

                                arr_val = game_array[square]
                                if arr_val == 1:
                                    print("\nYou have chosen: 1\n")
                                    current_player.score -= 1
                                elif arr_val == 2:
                                    print("\nYou have chosen: 2\n")
                                    for player in players:
                                        player.score -= 1
                                elif arr_val == 3:
                                    print("\nYou have chosen: 3\n")
                                    players[1 - players.index(current_player)].score -= 1
                                
                                game_array.pop(square)  # Remove the clicked square from the array
                                
                                growBranch(best_node_ind, square, game_array, player1.score, player2.score, lvl)

                                current_player = players[1 - players.index(current_player)]  # Switch turn to the other player
                                

        game_screen = pygame.Surface(screen.get_size())
        game_screen.fill(WHITE)
        print_players_score(game_screen, players)
        draw_squares(game_screen, game_array)  # Draw squares with numbers
        display_turn(game_screen, current_player)  # Display whose turn it is
        screen.blit(game_screen, (0, 0))
        pygame.display.flip()

        if not game_array:
            ind = 0
            break

    print_players_score(screen, players)
    pygame.display.flip()

    winner = analyze_win(players)
    return winner if winner != 'Draw' else 'draw'  # Return 'draw' if it's a tie


def display_winner(screen, winner):
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 36)
    
    if winner == 'draw':
        text_winner = font.render("It's a DRAW!", True, BLACK)
    elif winner == 'No one':
        text_winner = font.render("Hmm, and you won't even try?! Maybe you want to start again?", True, BLACK)
    else:
        text_winner = font.render(f"{winner} wins!", True, BLACK)
        
    text_rect_winner = text_winner.get_rect(center=screen.get_rect().center)
    screen.blit(text_winner, text_rect_winner)
    
    #if winner != 'draw':
    font_prompt = pygame.font.SysFont(None, 24)
    text_prompt = font_prompt.render("Press R to restart the game or Q to quit", True, BLACK)
    text_rect_prompt = text_prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
    screen.blit(text_prompt, text_rect_prompt)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'restart'
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


# Main function
def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    font = pygame.font.SysFont(None, 36)
    text = font.render("Welcome to our game!", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    font_button = pygame.font.SysFont(None, 30)
    text_start = font_button.render("Start", True, WHITE)
    text_rect_start = text_start.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    text_exit = font_button.render("Exit", True, WHITE)
    text_rect_exit = text_exit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    start_clicked = False
    # exit_clicked = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if text_rect_start.collidepoint(mouse_pos):
                    ind = 0
                    start_clicked = True
                elif text_rect_exit.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        if start_clicked:
            start_clicked = False
            while True:
                ind = 0
                winner = run_game(screen)
                
                if winner == 'restart':
                    break
                display_winner(screen, winner)
                action = display_winner(screen, winner)
                if action == 'restart':
                    break
                elif action == 'quit':
                    pygame.quit()
                    sys.exit()
        # After the game loop breaks, reset the click flag to False
            start_clicked = False
                    

        screen.fill(WHITE)
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, RED, (WIDTH // 2 - 50, HEIGHT // 2 - 20, 100, 40))
        screen.blit(text_start, text_rect_start)
        pygame.draw.rect(screen, RED, (WIDTH // 2 - 50, HEIGHT // 2 + 30, 100, 40))
        screen.blit(text_exit, text_rect_exit)
        pygame.display.flip()

if __name__ == "__main__":
    main()
