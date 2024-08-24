import pygame
import sys
from player import Player
from platforms import Platform
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700
START_HEIGHT = 200
BACKGROUND_COLOR = (173, 216, 230)
DARK_BLUE = (21, 34, 56)
BALL_COLOR = (255, 0, 0)
PLATFORM_COLOR = (255, 255, 255)
PLATFORM_WIDTH = 150
PLATFORM_SPACING = 200
GRAVITY = 2
DIFFICULTY = 1
FREE_FALL = 4
HIGH_SCORE = 0
START_TIME = 0
FPS = 60
platforms = []
MAX_PLATFORMS = 8

# Initialize game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rollaball")

# Initialize fonts
font = pygame.font.Font('game_font.ttf', 40)
subtext_font = pygame.font.Font('game_font.ttf', 20)
superscript_font = pygame.font.Font('game_font.ttf', 14)

# Create the player
player = Player(x=SCREEN_WIDTH // 2, y=START_HEIGHT, radius=20, color=BALL_COLOR, gravity=GRAVITY, free_fall=FREE_FALL)

# Set up a clock
clock = pygame.time.Clock()

# Create a new platform
def create_platform(y_pos):
    x_pos = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
    return Platform(x=x_pos,
                    y=y_pos,
                    width=PLATFORM_WIDTH,
                    color=PLATFORM_COLOR,
                    gravity=GRAVITY,
                    difficulty = DIFFICULTY)

def init_platforms():
    # Create starting platform
    start_platform = Platform(x=SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2,
                            y=START_HEIGHT + 20,
                            width=PLATFORM_WIDTH,
                            color=PLATFORM_COLOR,
                            gravity=GRAVITY,
                            difficulty = DIFFICULTY)
    platforms.append(start_platform)

    # Create the rest of the starting platforms
    for i in range(1, MAX_PLATFORMS):
        y_pos = START_HEIGHT + i * PLATFORM_SPACING + 20
        platforms.append(create_platform(y_pos))

# Helper function to wrap text
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        test_surface = font.render(test_line, True, DARK_BLUE)
        if test_surface.get_width() <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    lines.append(current_line)
    return lines

# Draw the starting screen
def draw_start_screen():
    screen.fill(BACKGROUND_COLOR)
    # Draw all platforms and player
    for platform in platforms:
        platform.draw(screen)
    player.draw(screen)

    # Draw the text
    start_text = "Don't touch the top or bottom!"
    wrapped_lines = wrap_text(start_text, font, SCREEN_WIDTH - 40)

    # Calculate total height of wrapped text block
    text_height = sum(font.get_linesize() for _ in wrapped_lines)
    
    # Draw each line of text
    y_pos = 50
    for line in wrapped_lines:
        text_surface = font.render(line, True, DARK_BLUE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos + text_surface.get_height() // 2))
        screen.blit(text_surface, text_rect)
        y_pos += text_surface.get_height()

    instructions_text = subtext_font.render("Press any arrow key to begin", True, DARK_BLUE)
    instructions_rect = instructions_text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(instructions_text, instructions_rect)

    pygame.display.flip()

# Restart the game
def restart_game():
    global game_over
    game_over = False
    DIFFICULTY = 1
    reset()
    main_game_loop()

def reset():
    platforms.clear()
    player.reset()
    init_platforms()

def main_game_loop():
    global DIFFICULTY, PLATFORM_SPACING, MAX_PLATFORMS, HIGH_SCORE, START_TIME, game_over

    # Wait for an arrow key press to start the game
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    waiting_for_key = False

    start_time = pygame.time.get_ticks()
    START_TIME = start_time

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(BACKGROUND_COLOR)

        # Player updates
        keys = pygame.key.get_pressed()
        player.update(keys, SCREEN_WIDTH, platforms)
        player.draw(screen)

        if player.game_over():
            game_over = True
            break

        # Platform updates
        for platform in platforms:
            if platform.is_out_of_bounds():
                platforms.remove(platform)
                platform.kill()
            else:
                platform.update()
                platform.draw(screen)

        if len(platforms) < MAX_PLATFORMS:
            lowest_y = max(platform.y for platform in platforms)
            new_y_pos = lowest_y + PLATFORM_SPACING
            platforms.append(create_platform(new_y_pos))

         # Check if 15 seconds have passed and increase difficulty
        current_time = pygame.time.get_ticks()
        if (current_time - start_time) >= 15000:  # 15 seconds
            DIFFICULTY += 0.5
            PLATFORM_SPACING += 10
            player.update_difficulty(DIFFICULTY)
            for platform in platforms:
                platform.update_difficulty(DIFFICULTY)
            start_time = current_time

        # Score logic
        seconds_elapsed = (current_time - START_TIME) // 1000
        HIGH_SCORE = max(HIGH_SCORE, seconds_elapsed)

        # Display score at the top right
        score_text = superscript_font.render(f'Score: {seconds_elapsed}', True, DARK_BLUE)
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 10, 20))
        screen.blit(score_text, score_rect)

        # Display high score at the top left
        high_score_text = superscript_font.render(f'High Score: {HIGH_SCORE}', True, DARK_BLUE)
        high_score_rect = high_score_text.get_rect(topleft=(10, 20))
        screen.blit(high_score_text, high_score_rect)

        pygame.display.flip()
        clock.tick(FPS)

    # Game Over Screen
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    restart_game()
                    return

        screen.fill(BACKGROUND_COLOR)
        
        # Game Over Text
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(game_over_text, text_rect)
        
        # Restart Instructions
        restart_text = subtext_font.render("Press any arrow key to play again", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(restart_text, restart_text_rect)

        pygame.display.flip()

# Initialize platforms
init_platforms()

# Show the start screen
draw_start_screen()

# Start the main game loop
main_game_loop()
