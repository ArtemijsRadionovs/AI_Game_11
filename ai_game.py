# Nepieciešamās bibliotēkas un moduļu importēšana
import pygame # Tiek importēta Pygame bibliotēka, lai izveidotu spēles grafisko interfeisu
import sys # Tiek importēts sys modulis, lai būtu iespēja iziet no spēles
import random # Tiek importēts random modulis, lai ģenerētu nejaušus skaitļus
from tree_logic import selectMinMax, selectAlphaBeta, growBranch, getInd, nodes # Tiek importētas funkcijas no tree_logic.py faila, kas ir saistītas ar darbībām koka struktūrā
import time # Importēt laika moduli, lai mērītu algoritma darbības laiku

# Statiskie krāsu mainīgie
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_YELLOW = (255, 215, 0)

# Mainīgais uzvaras ceļa uzglabāšanai
PATH = []

# Tiek definēta spēlētāja klase ar vārdu un punktu skaitu kā atribūtiem
class Player:
    def __init__(self, name, score):
        self.name = name # Spēlētāja vārds (Player vai Computer)
        self.score = score # Spēlētāja punktu skaits

# Funkcija, lai ģenerētu masīvu
# Tiek atgriezts masīvs ar nejauši izvēlētām vērtībām no 1 līdz 3
# Masīva garums ir ievadīts kā arguments
def generate_array(length):
    value_array = {} # Vārdnīca, lai glabātu masīva vērtības ar atslēgām

    for i in range(length):
        value = random.randint(1, 3)
        value_array.update({(i+1):value}) # Pievienot vērtību vārdnīcai ar atslēgu sākot no 1 
    print("Generated array:")
    print(value_array) # Izdrukāt masīvu konsolē
    return value_array

# Funkcija, lai izdrukātu spēlētāju rezultātus uz ekrāna
def print_players_score(screen, players):
    font = pygame.font.SysFont(None, 24)
    for i, player in enumerate(players):
        text = font.render(f"{player.name} score: {player.score}", True, BLACK)
        screen.blit(text, (20, 20 + i * 30))


# Funkcija, lai parādītu, kura spēlētāja kārta ir
# Parādā "Turn: Player", ja cilvēks izpilda gājienu
# Parādā "Turn: Computer", ja dators izpilda gājienu
def display_turn(screen, current_player):
    font = pygame.font.SysFont(None, 24)
    if current_player.name == "Player":
        text = font.render("Turn: Player", True, BLACK)
    else:
        text = font.render("Turn: Computer", True, BLACK)
    text_rect = text.get_rect(topright=(screen.get_width() - 20, 20))
    screen.blit(text, text_rect)

# Funkcija, lai parādītu ievades lodziņu masīva garumam
# Atgriezt masīva garumu, ja ievadītais skaitlis ir starp 15 un 25
def enter_val_arr_len(screen):
    input_text = "" # Ievades teksts
    error_message = "" # Kļūdas ziņojums

    font = pygame.font.SysFont(None, 36)
    text = font.render("Enter Array Length (15-25):", True, BLACK)
    text_rect = text.get_rect(center=screen.get_rect().center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN: # Pārbaudīt, vai notika taustiņa nospiešana
                if event.key == pygame.K_RETURN: # Pārbaudīt, vai tika nospiests Enter
                    try:
                        n = int(input_text) # Pārveidot ievadīto tekstu par skaitli
                        if 15 <= n <= 25: # Pārbaudīt, vai ievadītais skaitlis ir starp 15 un 25
                            return n
                        else:
                            # Ja ievadītais skaitlis nav starp 15 un 25, parādīt kļūdas paziņojumu
                            error_message = "Wrong value! Enter a number between 15 and 25."
                    except ValueError:
                        # Ja ievadītais teksts nav skaitlis, parādīt kļūdas paziņojumu
                        error_message = "Not a number! Enter a number between 15 and 25."
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE: # Pārbaudīt, vai tika nospiests Backspace
                    input_text = input_text[:-1] # Izdzēst pēdējo ievadīto simbolu
                    error_message = ""
                else:
                    input_text += event.unicode # Pievienot ievadīto simbolu ievades tekstam

        screen.fill(WHITE)
        screen.blit(text, text_rect)

        # Parādīt ievadīto tekstu
        font = pygame.font.SysFont(None, 48)
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (text_rect.centerx - input_surface.get_width() // 2, text_rect.centery + 50))

        # Parādīt kļūdas paziņojumu, ja tāds ir
        if error_message:
            error_font = pygame.font.SysFont(None, 35)
            error_text = error_font.render(error_message, True, RED)
            error_text_rect = error_text.get_rect(center=(text_rect.centerx, text_rect.centery + 100))
            screen.blit(error_text, error_text_rect)
        
        pygame.display.flip() # Atjaunot ekrānu
            
# Funkcija, lai analizētu uzvaru un atgrieztu uzvarētāja vārdu atkarībā no spēlētāju rezultātiem
# Ja spēles rezultāts ir neizšķirts, atgriezt "Draw"
def analyze_win(players):
    if players[0].score > players[1].score: # Pārbaudīt, vai pirmais spēlētājs ir uzvarējis
        return players[0].name
    elif players[0].score < players[1].score: # Pārbaudīt, vai otrais spēlētājs ir uzvarējis
        return players[1].name
    else: # Citādi ir neizšķirta spēle
        return "Draw"

# Funkcija, lai izvēlētos, kurš sāks spēli
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

    # Aprēķināt pogu un teksta kopējo augstumu
    total_height = button_height * 2 + button_margin

    # Aprēķināt pogas un teksta sākuma y pozīciju
    start_y = (starter_choice_screen.get_height() - total_height) // 2

    button_x = (screen.get_width() - button_width) // 2

    # Teksta un pogu pozīcijas pielāgošana
    text_rect_starter_choice.y = start_y

    # Poga "Player"
    button_y_player = start_y + text_rect_starter_choice.height + button_margin
    text_player_button = button_font.render("Player", True, WHITE)
    text_rect_player_button = text_player_button.get_rect(center=(button_x + button_width // 2, button_y_player + button_height // 2))
    pygame.draw.rect(starter_choice_screen, RED, (button_x, button_y_player, button_width, button_height))
    starter_choice_screen.blit(text_player_button, text_rect_player_button)

    # Poga "Computer"
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
            elif event.type == pygame.MOUSEBUTTONDOWN: # Pārbaudīt, vai notika peles klikšķis
                mouse_pos = pygame.mouse.get_pos() # Nolasīt peles pozīciju
                if text_rect_player_button.collidepoint(mouse_pos): # Pārbaudīt, vai notika peles klikšķis uz "Player" pogas
                    # Ja notika peles klikšķis uz "Player" pogas, tad sāks spēlētājs (cilvēks)
                    starter_choice = "Player"
                elif text_rect_computer_button.collidepoint(mouse_pos): # Pārbaudīt, vai notika peles klikšķis uz "Computer" pogas
                    # Ja notika peles klikšķis uz "Computer" pogas, tad sāks dators
                    starter_choice = "Computer"

    return starter_choice

# Funkcija, lai izvēlētos algoritmu
def choose_algorithm(screen):
    algorithm_choice = None
    algorithm_choice_screen = pygame.Surface(screen.get_size())
    algorithm_choice_screen.fill(WHITE)
    
    # Teksts "Choose algorithm:"
    font = pygame.font.SysFont(None, 36)
    text_algorithm_choice = font.render("Choose algorithm:", True, BLACK)
    text_rect_algorithm_choice = text_algorithm_choice.get_rect(center=algorithm_choice_screen.get_rect().center)
    text_rect_algorithm_choice.y -= 55
    algorithm_choice_screen.blit(text_algorithm_choice, text_rect_algorithm_choice)
    
    # Pogas parametri
    button_font = pygame.font.SysFont(None, 30)
    button_width = 145
    button_height = 50
    button_margin = 20
    button_padding = 15  # Pievienota atkāpe starp pogām
    
    # Pogas pozīcija
    button_x = (algorithm_choice_screen.get_width() - button_width) // 2

    button_y_minmax = text_rect_algorithm_choice.bottom + button_margin
    button_y_alphabeta = button_y_minmax + button_height + button_padding  # Pielāgota pozīcija
    
    # Poga "MinMax"
    text_minmax_button = button_font.render("MinMax", True, WHITE)
    text_rect_minmax_button = text_minmax_button.get_rect(center=(button_x + button_width // 2, button_y_minmax + button_height // 2))

    # Poga "Alpha-beta"
    text_alphabeta_button = button_font.render("Alpha-beta", True, WHITE)
    text_rect_alphabeta_button = text_alphabeta_button.get_rect(center=(button_x + button_width // 2, button_y_alphabeta + button_height // 2))

    # Teksta un pogu attēlošana uz ekrāna
    pygame.draw.rect(algorithm_choice_screen, RED, (button_x, button_y_minmax, button_width, button_height))
    algorithm_choice_screen.blit(text_minmax_button, text_rect_minmax_button)
    pygame.draw.rect(algorithm_choice_screen, RED, (button_x, button_y_alphabeta, button_width, button_height))  # Pielāgota pozīcija
    algorithm_choice_screen.blit(text_alphabeta_button, text_rect_alphabeta_button)

    screen.blit(algorithm_choice_screen, (0, 0))
    pygame.display.flip()

    while not algorithm_choice:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if text_rect_minmax_button.collidepoint(mouse_pos): # Pārbaudīt, vai notika peles klikšķis uz "MinMax" pogas
                    algorithm_choice = "MinMax" # Ja notika peles klikšķis uz "MinMax" pogas, tad izvēlēts MinMax algoritms
                elif text_rect_alphabeta_button.collidepoint(mouse_pos): # Pārbaudīt, vai notika peles klikšķis uz "Alpha-beta" pogas
                    algorithm_choice = "Alpha-beta" # Ja notika peles klikšķis uz "Alpha-beta" pogas, tad izvēlēts Alpha-beta algoritms

    return algorithm_choice

# Funkcija, lai uzzīmētu kvadrātus ar skaitļiem
def draw_squares(screen, squares):
    font = pygame.font.SysFont(None, 50)
    
    square_rects = {}  # Vārdnīca, lai glabātu kvadrātu taisnstūrus
    for i, (x, value) in enumerate(squares.items(), start=1):
        square_text = font.render(str(value), True, DARK_YELLOW)
        square_rect = square_text.get_rect(center=(x * 35, 120))
        pygame.draw.rect(screen, RED, square_rect)
        screen.blit(square_text, square_rect)
        
        square_rects[x] = square_rect  # Glabāt kvadrātu taisnstūrus vārdnīcā ar kvadrāta numuru kā atslēgu
    return square_rects

# Funkcija, kas palaiž algoritmu, lai izvēlētos kvadrātu
def computer_use_algorithm(algorithm_choice, ind):
    
    if algorithm_choice == "MinMax": # Ja izvēlēts MinMax algoritms
        tree_elem, tree_ind, tree_rating = selectMinMax(ind, True) # Izvēlēties labāko gājienu, izmantojot MinMax algoritmu
        best_node_ind = nodes[tree_ind]['ind'] # Izvēlētās virsotnes indekss
        print("Best node:", best_node_ind)
        square = nodes[best_node_ind]['elem'] # Izvēlētais kvadrāts
        lvl = nodes[best_node_ind]['lvl'] # Izvēlētās virsotnes līmenis

        for i in nodes: # Izdrukāt visus koka elementus
            print(nodes[i])

        return square, lvl, best_node_ind # Atgriezt izvēlēto kvadrātu, līmeni un virsotnes indeksu
        
    elif algorithm_choice == "Alpha-beta": # Ja izvēlēts Alpha-beta algoritms
        tree_elem, tree_ind, tree_rating = selectAlphaBeta(ind, float('-inf'), float('inf'), True) # Izvēlēties labāko gājienu, izmantojot Alpha-beta algoritmu
        best_node_ind = nodes[tree_ind]['ind']
        print("Best node:", best_node_ind)
        square = nodes[best_node_ind]['elem']
        lvl = nodes[best_node_ind]['lvl']

        for i in nodes:
            print(nodes[i])

        return square, lvl, best_node_ind


# Funkcija, lai atjaunotu spēlētāja rezultātu
def player_score_update(players, current_player, game_array, square): 
    arr_val = game_array[square] # Izvēlētā kvadrāta vērtība
    if arr_val == 1: # Ja kvadrāta vērtība ir 1
        print("\nYou have chosen: 1\n")
        current_player.score -= 1 # Atņemt 1 punktu no izvēlētā spēlētāja
    elif arr_val == 2: # Ja kvadrāta vērtība ir 2
        print("\nYou have chosen: 2\n")
        for player in players: # Atņemt 1 punktu no abiem spēlētājiem
            player.score -= 1
    elif arr_val == 3: # Ja kvadrāta vērtība ir 3
        print("\nYou have chosen: 3\n")
        players[1 - players.index(current_player)].score -= 1 # Atņemt 1 punktu no pretējā spēlētāja
    
    PATH.append((square, arr_val)) # Pievienot izvēlēto kvadrātu un vērtību uzvaras ceļam
    game_array.pop(square)  # Nodzēst izvēlēto kvadrātu no spēles masīva

# Funkcija, lai palaistu spēli
def run_game(screen):
    # Spēlētāju izveide
    player1 = Player("Player", 50)
    player2 = Player("Computer", 50)
    players = [player1, player2] # Spēlētāju saraksts

    array_length = enter_val_arr_len(screen)  # Ievadīt masīva garumu
    game_array = generate_array(array_length) # Izveidot masīvu ar garumu array_length un aizpildītu ar nejaušām vērtībām no 1 līdz 3
    
    ind = 0 # Sākuma virsotnes indekss
    ind = getInd() # Dabūt nākamo virsotnes indeksu
    growBranch(ind, 0, game_array, player1.score, player2.score, 0) # Uzcelt koku ar visiem iespējamiem gājieniem līdz dziļumam 3
    for i in nodes: # Izdrukāt visus koka elementus
        print(nodes[i])
    
    global PATH 
    
    starter_choice = choose_starter(screen) # Izvēlēties, kurš sāks spēli
    if starter_choice == "Computer": # Ja sāks dators
        current_player = player2 # Izmainīt gājienu uz datoru
    else:
        current_player = player1 # Citādi sāks spēlētājs

    algorithm_choice = choose_algorithm(screen) # Izvēlēties algoritmu
    print("Chosen algorithm:", algorithm_choice) 
    square_rects = draw_squares(screen, game_array) # Uzzīmēt kvadrātus ar skaitļiem

    running = True


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                ind = 0
                return 'No one' # Atgriezt "No one", ja spēlētājs iziet no spēles pirms uzvarētāja noteikšanas

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for square, square_rect in square_rects.items(): 
                    
                    if square_rect.collidepoint(mouse_pos):  # Pārbaudīt, vai kvadrāts ir nospiests
                        if square in game_array:  # Pārbaudīt, vai kvadrāts ir spēles masīvā
                            if current_player.name == "Player": # Ja ir spēlētāja gājiens
                                
                                player_score_update(players, current_player, game_array, square) # Atjaunot spēlētāja rezultātu
                                
                                element = nodes[ind]['elem'] # Atrast elementu, kas atbilst kvadrātam
                                if element == square: # Ja elements ir vienāds ar kvadrātu
                                    ind = nodes['ind'] # Izvēlēties jauno virsotni
                                
                                growBranch(ind, square, game_array, player1.score, player2.score, 0) # Uzcelt koku sākot no jaunās virsotnes
                                
                                current_player = players[1 - players.index(current_player)]  # Izmainīt gājienu uz otru spēlētāju
                                # Tajā pašā klikšķī palaist algoritmu, lai dators izvēlētos kvadrātu
                                if current_player.name == "Computer": 
                                    if game_array:  # Pārbaudīt, vai spēles masīvs nav tukšs
                                        start_time = time.time()
                                        square, lvl, best_node_ind = computer_use_algorithm(algorithm_choice, ind) # Izvēlēties kvadrātu, izmantojot izvēlēto algoritmu

                                        player_score_update(players, current_player, game_array, square) # Atjaunot spēlētāja rezultātu

                                        end_time = time.time()
                                        print("Time taken for turn:", end_time - start_time)
                                        
                                        growBranch(best_node_ind, square, game_array, player1.score, player2.score, lvl) # Uzcelt koku sākot no jaunās virsotnes

                                        current_player = players[1 - players.index(current_player)]  # Izmainīt gājienu uz otru spēlētāju
                            
                            elif current_player.name == "Computer": # Ja dators uzsāk spēli, tad palaist algoritmu, lai dators izvēlētos kvadrātu pirmais
                                start_time = time.time()
                                square, lvl, best_node_ind = computer_use_algorithm(algorithm_choice, ind) # Izvēlēties kvadrātu, izmantojot izvēlēto algoritmu
                                
                                player_score_update(players, current_player, game_array, square) # Atjaunot spēlētāja rezultātu

                                end_time = time.time()
                                print("Time taken for turn:", end_time - start_time)
                                
                                growBranch(best_node_ind, square, game_array, player1.score, player2.score, lvl) # Uzcelt koku sākot no jaunās virsotnes

                                current_player = players[1 - players.index(current_player)]  # Izmainīt gājienu uz otru spēlētāju
                                

        game_screen = pygame.Surface(screen.get_size()) 
        game_screen.fill(WHITE)
        print_players_score(game_screen, players) # Parādīt spēlētāju rezultātus uz ekrāna
        draw_squares(game_screen, game_array)     # Uzzīmēt kvadrātus ar skaitļiem
        display_turn(game_screen, current_player) # Parādīt kvadrātus ekranā
        screen.blit(game_screen, (0, 0))
        pygame.display.flip()

        if not game_array: # Pārbaudīt, vai spēles masīvs ir tukšs
            ind = 0
            break

    print_players_score(screen, players) # Parādīt spēlētāju rezultātus uz ekrāna
    pygame.display.flip()

    winner = analyze_win(players) # Noteikt uzvarētāju
    return winner if winner != 'Draw' else 'draw'  # Atgriezt uzvarētāju, ja nav neizšķirta spēle

# Funkcija, lai parādītu uzvarētāju un piedāvātu restartēt vai iziet no spēles
# Atgriež 'restart', ja spēle ir jārestartē, 'quit', ja spēle ir jāiziet, 
# 'draw', ja ir neizšķirta spēle un 'No one', ja spēlētājs iziet no spēles pirms uzvarētāja noteikšanas

def display_winner(screen, winner):
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 36)
    
    if winner == 'draw': # Ja ir neizšķirta spēle
        text_winner = font.render("It's a DRAW!", True, BLACK) # Parādīt, ka ir neizšķirta spēle
    elif winner == 'No one': # Ja spēlētājs iziet no spēles pirms uzvarētāja noteikšanas
        text_winner = font.render("Hmm, and you won't even finish the game?! Maybe you want to start again?", True, BLACK) 
    else:
        text_winner = font.render(f"{winner} wins!", True, BLACK) # Parādīt uzvarētāju
        
    text_rect_winner = text_winner.get_rect(center=screen.get_rect().center)
    screen.blit(text_winner, text_rect_winner)
    
    # Parādīt tekstu, lai redzētu, kā restartēt vai iziet no spēles
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
                if event.key == pygame.K_r: # Ja nospiež 'R', tad restartēt spēli
                    return 'restart'
                elif event.key == pygame.K_q: # Ja nospiež 'Q', tad iziet no spēles
                    pygame.quit()
                    sys.exit()


# Galvenās spēles funkcija, kur tiek inicializēts Pygame un palaista spēle
def main():
    pygame.init()
    WIDTH, HEIGHT = 1000, 600 # Ekrāna izmēri
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Izveidot ekrānu
    pygame.display.set_caption("The AI Game") # Iestatīt ekrāna nosaukumu

    # Sākuma ekrāna izveide

    font = pygame.font.SysFont(None, 36)
    text = font.render("Welcome to our game!", True, BLACK) 
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    
    font_button = pygame.font.SysFont(None, 30) # Pogas fonta izmērs

    # "Start" pogas teksts un taisnstūra pozīcija
    text_start = font_button.render("Start", True, WHITE)
    text_rect_start = text_start.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # "Exit" pogas teksts un taisnstūra pozīcija
    text_exit = font_button.render("Exit", True, WHITE)
    text_rect_exit = text_exit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    global PATH # Globalais mainīgais, lai uzglabātu uzvarētāja ceļu
    start_clicked = False

    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if text_rect_start.collidepoint(mouse_pos): # Pārbaudīt, vai peles klikšķis bija uz "Start" pogas
                    start_clicked = True
                elif text_rect_exit.collidepoint(mouse_pos): # Pārbaudīt, vai peles klikšķis bija uz "Exit" pogas
                    pygame.quit()
                    sys.exit()

        if start_clicked: # Ja "Start" poga ir noklikšķināta
            start_clicked = False
            while True:
                winner = run_game(screen) # Palaist spēli
                print("Winning path: ")
                print(PATH) # Izdrukāt uzvarētāja ceļu pēc spēles beigām
                PATH = []
                if winner == 'restart':
                    break
                # Parādīt uzvarētāju un piedāvāt restartēt vai iziet no spēles
                action = display_winner(screen, winner) 
                if action == 'restart': # Ja nospiež 'R', tad restartēt spēli
                    break
                elif action == 'quit': # Ja nospiež 'Q', tad iziet no spēles
                    pygame.quit()
                    sys.exit()
        # Pēc spēles cikla pārtraukšanas atiestatīt klikšķa karodziņu uz False
            start_clicked = False
                    
        # Šeit tiek uzzīmēts sākuma ekrāns
        screen.fill(WHITE)
        
        # Parādīt "Start" un "Exit" pogas uz ekrāna
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, RED, (WIDTH // 2 - 50, HEIGHT // 2 - 20, 100, 40))
        screen.blit(text_start, text_rect_start)
        
        pygame.draw.rect(screen, RED, (WIDTH // 2 - 50, HEIGHT // 2 + 30, 100, 40))
        screen.blit(text_exit, text_rect_exit)
        pygame.display.flip()

if __name__ == "__main__":
    main()
