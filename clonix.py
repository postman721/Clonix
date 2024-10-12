#Copyright (c) 2024 JJ Posti <techtimejourney.net>
#This program comes with ABSOLUTELY NO WARRANTY; for details see: GNU GPL.
#This is free software, and you are welcome to redistribute it under GPL Version 2, June 1991.

import pygame
import random
import os
import pickle  # Import pickle for high score management

# Initialize pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
BLOCK_SIZE = 40
PLAY_WIDTH = 12 * BLOCK_SIZE
PLAY_HEIGHT = 24 * BLOCK_SIZE
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2 - 100
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 20

# File to store high score
HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), 'high_score.pkl')

# Load Images
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')

if not os.path.exists(ASSETS_PATH):
    raise Exception("Assets directory not found. Please create an 'assets' folder with required images.")

# Load background image
try:
    BACKGROUND_IMG = pygame.image.load(os.path.join(ASSETS_PATH, 'background.png'))
    BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))
except FileNotFoundError:
    BACKGROUND_IMG = None
    print("Background image not found. Proceeding without background.")

# Load tetromino images
SHAPE_IMAGES = {}
shape_names = ['S', 'Z', 'I', 'O', 'J', 'L', 'T']
for shape in shape_names:
    try:
        img = pygame.image.load(os.path.join(ASSETS_PATH, f'{shape}.png'))
        img = pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))
        SHAPE_IMAGES[shape] = img
    except FileNotFoundError:
        SHAPE_IMAGES[shape] = None
        print(f"Image for shape '{shape}' not found. Using colored blocks instead.")

# Shapes
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# List of shapes
SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# Define the Piece class
class Piece:
    def __init__(self, x, y, shape_id):
        self.x = x
        self.y = y
        self.shape_id = shape_id
        self.shape = SHAPES[shape_names.index(shape_id)]
        self.color = SHAPE_COLORS[shape_names.index(shape_id)]
        self.image = SHAPE_IMAGES[shape_id]
        self.rotation = 0  # current rotation state

# High Score Functions using pickle
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'rb') as file:
            return pickle.load(file)
    return 0  # If no file exists, return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'wb') as file:
        pickle.dump(score, file)

def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(12)] for _ in range(24)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))

    return positions

def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(12) if grid[y][x] == (0, 0, 0)] for y in range(24)]
    accepted_positions = [x for sub in accepted_positions for x in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    shape_id = random.choice(shape_names)
    return Piece(5, 0, shape_id)

def draw_text_middle(surface, text, size, color, alpha=255):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    label_surface = pygame.Surface(label.get_size(), pygame.SRCALPHA)
    label_surface.fill((255, 255, 255, 0))
    label_surface.blit(label, (0, 0))
    label_surface.set_alpha(alpha)

    surface.blit(label_surface, (SCREEN_WIDTH / 2 - label.get_width() / 2, SCREEN_HEIGHT / 2 - label.get_height() / 2))

def fade_out_text(surface, text, size, color, duration=5000):
    fade_steps = 50
    delay = duration // fade_steps
    for alpha in range(255, 0, -int(255/fade_steps)):
        surface.fill((30, 30, 30))
        draw_text_middle(surface, text, size, color, alpha)
        pygame.display.update()
        pygame.time.delay(delay)

def draw_grid(surface, grid):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y
    for y in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + y * BLOCK_SIZE), (sx + PLAY_WIDTH, sy + y * BLOCK_SIZE))
        for x in range(len(grid[y])):
            pygame.draw.line(surface, (128, 128, 128), (sx + x * BLOCK_SIZE, sy), (sx + x * BLOCK_SIZE, sy + PLAY_HEIGHT))

def clear_rows(grid, locked, surface):
    inc = 0
    for y in range(len(grid)-1, -1, -1):
        row = grid[y]
        if (0, 0, 0) not in row:
            inc += 1
            for x in range(len(row)):
                del locked[(x, y)]
            # Animate the row fading out
            animate_clear_row(surface, grid, y)
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < inc:
                continue
            new_key = (x, y - inc)
            locked[new_key] = locked.pop(key)
    return inc

def animate_clear_row(surface, grid, row):
    """ Animate the clearing of a row by fading it out """
    fade_steps = 10
    for alpha in range(255, 0, -int(255/fade_steps)):
        for x in range(12):
            pygame.draw.rect(surface, (255, 255, 255, alpha), (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.update()
        pygame.time.delay(50)

def draw_window(surface, grid, score=0, last_score=0, next_piece=None):
    if BACKGROUND_IMG:
        surface.blit(BACKGROUND_IMG, (0, 0))
    else:
        surface.fill((30, 30, 30))

    # Current Score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    
    sx = TOP_LEFT_X + PLAY_WIDTH + 20
    sy = TOP_LEFT_Y + PLAY_HEIGHT - 150
    
    surface.blit(label, (sx, sy))
    
    # High Score
    label = font.render('High Score: ' + str(last_score), 1, (255, 255, 255))
    
    surface.blit(label, (sx, sy + 30))
    
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != (0, 0, 0):
                pygame.draw.rect(surface, grid[y][x], (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

    # Draw next shape
    if next_piece:
        draw_next_shape(surface, next_piece)

def draw_next_shape(surface, next_piece):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + 200
    format = next_piece.shape[next_piece.rotation % len(next_piece.shape)]

    surface.blit(label, (sx + 10, sy - 30))

    for i, line in enumerate(format):
        for j, column in enumerate(list(line)):
            if column == '0':
                pygame.draw.rect(surface, next_piece.color,
                                 (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)
    
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()  # Track next shape
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.3  # Start with a faster speed
    speed_increase_interval = 5  # Time in seconds to increase speed (changed to 5 seconds)
    level_time = 0
    score = 0
    high_score = load_high_score()  # Load high score at the start
    
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick(60)  # Run the game at 60 FPS

        # Increase speed every 5 seconds (speed_increase_interval = 5)
        if level_time / 1000 > speed_increase_interval:
            level_time = 0
            if fall_speed > 0.1:  # Minimum cap on speed
                fall_speed -= 0.02  # Speed up the game by 0.02 (instead of 0.01)
        
        # Handle piece falling
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # Handle player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)

        shape_pos = convert_shape_format(current_piece)

        # Place the piece on the grid
        for pos in shape_pos:
            x, y = pos
            if y > -1:
                grid[y][x] = current_piece.color

        # Lock the piece in place
        if change_piece:
            for pos in shape_pos:
                locked_positions[pos] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()  # Update the next shape
            change_piece = False
            score += clear_rows(grid, locked_positions, win) * 10

        draw_window(win, grid, score, high_score, next_piece)
        pygame.display.update()

        if check_lost(locked_positions):
            fade_out_text(win, "YOU LOST!", 80, (255, 255, 255), 5000)
            run = False
            # Save the high score if the player achieves a new high score
            if score > high_score:
                save_high_score(score)
            main_menu(win)  # After losing, return to the main menu

def main_menu(win):
    run = True
    while run:
        if BACKGROUND_IMG:
            win.blit(BACKGROUND_IMG, (0, 0))
        else:
            win.fill((30, 30, 30))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.quit()

# Create the game window
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Clonix')

main_menu(win)
