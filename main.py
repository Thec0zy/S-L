import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 600, 600
BACKGROUND_COLOR = (0, 0, 0)

# Load sound effects
click_sound = pygame.mixer.Sound("sounds/Click.mp3")
roll_sound = pygame.mixer.Sound("sounds/Roll.mp3")
song1_sound = pygame.mixer.Sound("sounds/Song1.mp3")
song_sound = pygame.mixer.Sound("sounds/Song.mp3")
win_sound = pygame.mixer.Sound("sounds/Win.mp3")

# Load board images for selection screen
easy_board = pygame.image.load("images/easy.jpg")
medium_board = pygame.image.load("images/medium.jpg")
hard_board = pygame.image.load("images/hard.jpg")
easy_board = pygame.transform.scale(easy_board, (130, 130))
medium_board = pygame.transform.scale(medium_board, (130, 130))
hard_board = pygame.transform.scale(hard_board, (130, 130))

# Load and resize board images for game screen
easy_boardG = pygame.transform.scale(pygame.image.load("images/easy.jpg"), (400, 400))
medium_boardG = pygame.transform.scale(pygame.image.load("images/medium.jpg"), (400, 400))
hard_boardG = pygame.transform.scale(pygame.image.load("images/hard.jpg"), (400, 400))

# Position for boards in selection screen
easy_rect = easy_board.get_rect(topleft=(60, 200))
medium_rect = medium_board.get_rect(topleft=(210, 200))
hard_rect = hard_board.get_rect(topleft=(360, 200))

# Load player images for tokens and player info
player_images = [
    pygame.transform.scale(pygame.image.load(f"images/player{i}.jpg"), (20, 20)) for i in range(1, 5)
]
player_images_large = [
    pygame.transform.scale(pygame.image.load(f"images/player{i}.jpg"), (30, 30)) for i in range(1, 5)
]

# Board sizes and constants
BOARD_SIZES = {"Easy": 16, "Medium": 36, "Hard": 64}
BOARD_DIMENSIONS = {"Easy": 4, "Medium": 6, "Hard": 8}
SNAKES_LADDERS = {
    "Easy": {5: 10, 6: 0, 11: 3, 8: 14},
    "Medium": {1: 8, 6: 17, 10: 22, 21: 7, 20: 26, 24: 35, 28: 17, 33: 23},
    "Hard": {1: 14, 2: 12, 8: 24, 18: 29, 19: 4, 20: 6, 21: 35, 30: 16, 
             34: 28, 37: 25, 38: 54, 40: 24, 48: 62, 49: 35, 52: 59, 57: 43}
}

# Initialize fonts
pygame.font.init()
font = pygame.font.Font(None, 36)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("S&L")

# Play Song1 at start
song1_sound.play(loops=-1)

# Global variables
selected_board = None
selected_players = None
die_images = [pygame.transform.scale(pygame.image.load(f"images/die{i}.jpg"), (50, 50)) for i in range(1, 7)]
die_result = 0
player_positions = [0] * 4
current_player = 0
winner = None

# Frame with moving lights effect helper function
def draw_moving_lights_frame(screen, frame_counter):
    light_size = 10
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    for i in range(0, WIDTH, light_size * 2):  # Top and bottom
        color = colors[(i // (light_size * 2) + frame_counter) % len(colors)]
        pygame.draw.rect(screen, color, (i, 0, light_size, light_size))  # Top
        pygame.draw.rect(screen, color, (i, HEIGHT - light_size, light_size, light_size))  # Bottom
    for i in range(0, HEIGHT, light_size * 2):  # Left and right
        color = colors[(i // (light_size * 2) + frame_counter) % len(colors)]
        pygame.draw.rect(screen, color, (0, i, light_size, light_size))  # Left
        pygame.draw.rect(screen, color, (WIDTH - light_size, i, light_size, light_size))  # Right

def welcome_screen():
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, 40)  # Reduced from 50 to fit longer text
    button_font = pygame.font.Font(None, 40)
    
    title_text = font.render("Welcome to S&L", True, (255, 255, 255))
    title_text2 = font.render("Snake and Ladder Board Game", True, (255, 255, 255))
    play_text = button_font.render("Play", True, (0, 0, 0))
    exit_text = button_font.render("Exit", True, (0, 0, 0))

    play_button = pygame.Rect(200, 250, 200, 60)
    exit_button = pygame.Rect(200, 350, 200, 60)

    frame_counter = 0  # For light animation
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_moving_lights_frame(screen, frame_counter)  # Draw animated frame
        screen.blit(title_text, (180, 100))  # Adjusted x to 50 to fit longer text
        screen.blit(title_text2, (90, 150))
        pygame.draw.rect(screen, (0, 255, 0), play_button, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), exit_button, border_radius=10)
        screen.blit(play_text, (play_button.x + 70, play_button.y + 15))
        screen.blit(exit_text, (exit_button.x + 75, exit_button.y + 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_button.collidepoint(x, y):
                    click_sound.play()
                    running = False
                    player_selection_screen()
                elif exit_button.collidepoint(x, y):
                    click_sound.play()
                    pygame.quit()
                    exit()

        frame_counter = (frame_counter + 1) % 60  # Cycle through animation
        pygame.display.flip()
        clock.tick(30)  # Control frame rate for smooth animation

def player_selection_screen():
    global selected_players
    font = pygame.font.Font(None, 40)
    button_font = pygame.font.Font(None, 40)

    title_text = font.render("Select Number of Players", True, (255, 255, 255))
    single_player_text = button_font.render("Single Player", True, (255, 255, 255))
    two_players_text = button_font.render("Two players", True, (255, 255, 255))
    three_players_text = button_font.render("Three players", True, (255, 255, 255))
    four_players_text = button_font.render("Four Players", True, (255, 255, 255))
    back_text = button_font.render("Back", True, (0, 0, 0))

    single_player_button = pygame.Rect(200, 150, 200, 60)
    two_players_button = pygame.Rect(200, 250, 200, 60)
    three_players_button = pygame.Rect(200, 350, 200, 60)
    four_players_button = pygame.Rect(200, 450, 200, 60)
    back_button = pygame.Rect(20, 25, 100, 40)

    frame_counter = 0
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_moving_lights_frame(screen, frame_counter)
        screen.blit(title_text, (140, 90))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_hover_color = (0, 255, 0)  # Green for hover
        button_default_color = (50, 50, 50)  # Gray for default
        back_hover_color = (255, 200, 0)  # Brighter orange for back button hover
        back_default_color = (255, 165, 0)  # Normal orange for back button

        # Apply hover effect to player selection buttons
        pygame.draw.rect(screen, button_hover_color if single_player_button.collidepoint(mouse_x, mouse_y) else button_default_color, single_player_button, border_radius=10)
        pygame.draw.rect(screen, button_hover_color if two_players_button.collidepoint(mouse_x, mouse_y) else button_default_color, two_players_button, border_radius=10)
        pygame.draw.rect(screen, button_hover_color if three_players_button.collidepoint(mouse_x, mouse_y) else button_default_color, three_players_button, border_radius=10)
        pygame.draw.rect(screen, button_hover_color if four_players_button.collidepoint(mouse_x, mouse_y) else button_default_color, four_players_button, border_radius=10)
        pygame.draw.rect(screen, back_hover_color if back_button.collidepoint(mouse_x, mouse_y) else back_default_color, back_button, border_radius=10)

        screen.blit(single_player_text, (single_player_button.x + 14, single_player_button.y + 15))
        screen.blit(two_players_text, (two_players_button.x + 20, two_players_button.y + 15))
        screen.blit(three_players_text, (three_players_button.x + 12, three_players_button.y + 15))
        screen.blit(four_players_text, (four_players_button.x + 18, four_players_button.y + 15))
        screen.blit(back_text, (back_button.x + 15, back_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if single_player_button.collidepoint(x, y):
                    click_sound.play()
                    selected_players = 1
                    running = False
                    board_selection_screen()
                elif two_players_button.collidepoint(x, y):
                    click_sound.play()
                    selected_players = 2
                    running = False
                    board_selection_screen()
                elif three_players_button.collidepoint(x, y):
                    click_sound.play()
                    selected_players = 3
                    running = False
                    board_selection_screen()
                elif four_players_button.collidepoint(x, y):
                    click_sound.play()
                    selected_players = 4
                    running = False
                    board_selection_screen()
                elif back_button.collidepoint(x, y):
                    click_sound.play()
                    running = False
                    welcome_screen()

        frame_counter = (frame_counter + 1) % 60
        pygame.display.flip()
        clock.tick(30)

def board_selection_screen():
    global selected_board
    screen.fill(BACKGROUND_COLOR)

    font = pygame.font.Font(None, 40)
    font2 = pygame.font.Font(None, 30)

    title_textB = font.render("Please select a board", True, (255, 255, 255))
    easy_text = font2.render("Easy", True, (255, 255, 255))
    medium_text = font2.render("Medium", True, (255, 255, 255))
    hard_text = font2.render("Hard", True, (255, 255, 255))

    easy_button_rect = pygame.Rect(60, 350, 130, 40)
    medium_button_rect = pygame.Rect(210, 350, 130, 40)
    hard_button_rect = pygame.Rect(360, 350, 130, 40)
    back_button = pygame.Rect(20, 25, 100, 40)

    button_font = pygame.font.Font(None, 40)
    back_text = button_font.render("Back", True, (0, 0, 0))

    frame_counter = 0
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_moving_lights_frame(screen, frame_counter)
        screen.blit(title_textB, (150, 100))
        screen.blit(easy_board, easy_rect.topleft)
        screen.blit(medium_board, medium_rect.topleft)
        screen.blit(hard_board, hard_rect.topleft)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_hover_color = (0, 255, 0)
        button_default_color = (50, 50, 50)

        pygame.draw.rect(screen, button_hover_color if easy_button_rect.collidepoint(mouse_x, mouse_y) else button_default_color, easy_button_rect, border_radius=10)
        pygame.draw.rect(screen, button_hover_color if medium_button_rect.collidepoint(mouse_x, mouse_y) else button_default_color, medium_button_rect, border_radius=10)
        pygame.draw.rect(screen, button_hover_color if hard_button_rect.collidepoint(mouse_x, mouse_y) else button_default_color, hard_button_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 165, 0), back_button, border_radius=10)

        screen.blit(easy_text, (easy_button_rect.x + 40, easy_button_rect.y + 10))
        screen.blit(medium_text, (medium_button_rect.x + 20, medium_button_rect.y + 10))
        screen.blit(hard_text, (hard_button_rect.x + 39, hard_button_rect.y + 10))
        screen.blit(back_text, (back_button.x + 15, back_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if easy_button_rect.collidepoint(x, y):
                    click_sound.play()
                    selected_board = "Easy"
                    song1_sound.stop()
                    running = False
                    game_screen()
                elif medium_button_rect.collidepoint(x, y):
                    click_sound.play()
                    selected_board = "Medium"
                    song1_sound.stop()
                    running = False
                    game_screen()
                elif hard_button_rect.collidepoint(x, y):
                    click_sound.play()
                    selected_board = "Hard"
                    song1_sound.stop()
                    running = False
                    game_screen()
                elif back_button.collidepoint(x, y):
                    click_sound.play()
                    running = False
                    player_selection_screen()

        frame_counter = (frame_counter + 1) % 60
        pygame.display.flip()
        clock.tick(30)

def get_square_coords(board_type, position, player_index=0):
    board_size = BOARD_DIMENSIONS[board_type]
    square_size = 400 // board_size
    board_x, board_y = 150, (HEIGHT - 400) // 2
    player_size = 20

    row = board_size - 1 - (position // board_size)
    col = position % board_size if row % 2 == 0 else (board_size - 1 - position % board_size)
    
    x = board_x + col * square_size + (square_size - player_size) // 2 + (player_index * 5)
    y = board_y + row * square_size + (square_size - player_size) // 2 + (player_index * 2)
    return (x, y)

def check_snakes_ladders(board_type, position):
    if position in SNAKES_LADDERS[board_type]:
        return SNAKES_LADDERS[board_type][position]
    return position

def game_screen():
    global die_result, current_player, player_positions, winner, selected_board, selected_players

    song_sound.play(loops=-1)
    is_muted = False

    roll_button = pygame.Rect(20, 500, 100, 50)
    quit_button = pygame.Rect(450, 10, 100, 40)
    mute_button = pygame.Rect(340, 10, 100, 40)
    play_again_button = pygame.Rect(150, 540, 100, 40)
    new_game_button = pygame.Rect(260, 540, 100, 40)
    exit_button = pygame.Rect(370, 540, 100, 40)

    button_font_large = pygame.font.Font(None, 30)
    button_font_small = pygame.font.Font(None, 24)
    player_font = pygame.font.Font(None, 24)  # Font for player names

    roll_text = button_font_large.render("Roll", True, (0, 0, 0))
    quit_text = button_font_large.render("Quit", True, (0, 0, 0))
    mute_text = button_font_large.render("Mute", True, (0, 0, 0))
    unmute_text = button_font_large.render("Unmute", True, (0, 0, 0))
    play_again_text = button_font_small.render("Play Again", True, (0, 0, 0))
    new_game_text = button_font_small.render("New Game", True, (0, 0, 0))
    exit_text = button_font_large.render("Exit", True, (0, 0, 0))

    board_dict = {"Easy": easy_boardG, "Medium": medium_boardG, "Hard": hard_boardG}
    board_surface = board_dict[selected_board]
    board_rect = board_surface.get_rect(topleft=(150, (HEIGHT - 400) // 2))

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Display player information on the left side
        for i in range(selected_players):
            player_text = player_font.render(f"Player {i+1}", True, (255, 255, 255))
            screen.blit(player_images_large[i], (10, 100 + i * 50))
            screen.blit(player_text, (45, 100 + i * 50 + 5))

        screen.blit(board_surface, board_rect.topleft)
        screen.blit(die_images[die_result], (20, 400))

        if winner is None:
            pygame.draw.rect(screen, (0, 255, 0), roll_button, border_radius=10)
            screen.blit(roll_text, (roll_button.x + 30, roll_button.y + 15))
        else:
            pygame.draw.rect(screen, (0, 255, 0), play_again_button, border_radius=10)
            pygame.draw.rect(screen, (0, 255, 0), new_game_button, border_radius=10)
            pygame.draw.rect(screen, (255, 0, 0), exit_button, border_radius=10)
            screen.blit(play_again_text, (play_again_button.x + 5, play_again_button.y + 10))
            screen.blit(new_game_text, (new_game_button.x + 5, new_game_button.y + 10))
            screen.blit(exit_text, (exit_button.x + 25, exit_button.y + 10))

        pygame.draw.rect(screen, (255, 0, 0), quit_button, border_radius=10)
        pygame.draw.rect(screen, (0, 255, 255), mute_button, border_radius=10)
        screen.blit(quit_text, (quit_button.x + 20, quit_button.y + 10))
        screen.blit(mute_text if not is_muted else unmute_text, 
                   (mute_button.x + (20 if not is_muted else 10), mute_button.y + 10))

        for i in range(selected_players):
            x, y = get_square_coords(selected_board, player_positions[i], i)
            screen.blit(player_images[i], (x, y))

        if winner is None and selected_players > 1:
            turn_text = font.render(f"Player {current_player + 1}'s Turn", True, (255, 255, 255))
            screen.blit(turn_text, (120, 50))
        elif winner is not None:
            win_text = font.render(f"Player {winner + 1} Wins!", True, (255, 255, 0))
            screen.blit(win_text, (120, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if winner is None and roll_button.collidepoint(x, y):
                    roll_sound.play()
                    die_result = random.randint(0, 5)
                    player_positions[current_player] += die_result + 1
                    if player_positions[current_player] >= BOARD_SIZES[selected_board] - 1:
                        player_positions[current_player] = BOARD_SIZES[selected_board] - 1
                        winner = current_player
                        song_sound.stop()
                        win_sound.play()
                    else:
                        player_positions[current_player] = check_snakes_ladders(selected_board, player_positions[current_player])
                        if player_positions[current_player] == BOARD_SIZES[selected_board] - 1:
                            winner = current_player
                            song_sound.stop()
                            win_sound.play()
                    if winner is None and selected_players > 1:
                        current_player = (current_player + 1) % selected_players
                elif quit_button.collidepoint(x, y):
                    click_sound.play()
                    pygame.quit()
                    exit()
                elif mute_button.collidepoint(x, y):
                    click_sound.play()
                    if is_muted:
                        song_sound.play(loops=-1)
                        is_muted = False
                    else:
                        song_sound.stop()
                        is_muted = True
                elif winner is not None:
                    if play_again_button.collidepoint(x, y):
                        click_sound.play()
                        player_positions = [0] * 4
                        current_player = 0
                        die_result = 0
                        winner = None
                        song_sound.play(loops=-1)
                        is_muted = False
                    elif new_game_button.collidepoint(x, y):
                        click_sound.play()
                        player_positions = [0] * 4
                        current_player = 0
                        die_result = 0
                        winner = None
                        selected_board = None
                        selected_players = None
                        running = False
                        song_sound.stop()
                        song1_sound.play(loops=-1)
                        player_selection_screen()
                    elif exit_button.collidepoint(x, y):
                        click_sound.play()
                        pygame.quit()
                        exit()

        pygame.display.flip()

# Main loop
welcome_screen()

