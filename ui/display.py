import os
import json
import pygame
from datetime import datetime

from clock.time_manager import get_current_time
from clock.word_mapper import map_time_to_words
from config import IS_DEV_MODE

# === Grundeinstellungen ===
CELL_SIZE = 60
GRID_WIDTH = 11
GRID_HEIGHT = 10
FONT_SIZE = 48
MARGIN = 10

# Farben
COLOR_BASE = (100, 100, 100)  # grau (inaktiv)
COLOR_TARGET = (255, 255, 255)  # weiß (aktiv)
BG_COLOR = (0, 0, 0)  # schwarz
FADE_SPEED = 3  # Geschwindigkeit der Helligkeitsanpassung

# === Grid-Daten laden ===
with open(os.path.join("assets", "grid_layout.json"), encoding="utf-8") as f:
    data = json.load(f)
    grid = data["grid"]
    words = data["words"]

def get_active_positions(active_words):
    active_positions = set()
    for word in active_words:
        for pos in words.get(word, []):
            active_positions.add(tuple(pos))
    return active_positions

def start_display():
    if IS_DEV_MODE:
        from ui.terminal_display import start_terminal_display
        start_terminal_display()
    else:
        # === Pygame Setup ===
        pygame.init()
        font = pygame.font.SysFont("monospace", FONT_SIZE)
        screen_width = GRID_WIDTH * CELL_SIZE + MARGIN * 2
        screen_height = GRID_HEIGHT * CELL_SIZE + MARGIN * 2
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Mundart Wortuhr")
        clock = pygame.time.Clock()

        now = get_current_time()
        current_minute = now.minute
        active_words = map_time_to_words(now.hour, now.minute)
        active_positions = get_active_positions(active_words)

        letter_intensity = {}
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                letter_intensity[(row, col)] = COLOR_BASE[0]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            now = datetime.now()
            if now.minute != current_minute:
                now_rounded = get_current_time()
                active_words = map_time_to_words(now_rounded.hour, now_rounded.minute)
                active_positions = get_active_positions(active_words)
                current_minute = now.minute

            screen.fill(BG_COLOR)

            for row in range(GRID_HEIGHT):
                for col in range(GRID_WIDTH):
                    pos = (row, col)
                    target_intensity = COLOR_TARGET[0] if pos in active_positions else COLOR_BASE[0]
                    current = letter_intensity[pos]

                    if current < target_intensity:
                        current = min(current + FADE_SPEED, target_intensity)
                    elif current > target_intensity:
                        current = max(current - FADE_SPEED, target_intensity)

                    letter_intensity[pos] = current

                    try:
                        letter = grid[row][col]
                    except IndexError:
                        continue

                    color = (current, current, current)
                    text = font.render(letter, True, color)
                    x = MARGIN + col * CELL_SIZE
                    y = MARGIN + row * CELL_SIZE
                    screen.blit(text, (x, y))

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    start_display()