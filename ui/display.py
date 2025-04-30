import os
import json
from clockpi.clock.time_manager import get_current_time
from clockpi.clock.word_mapper import map_time_to_words
from clockpi.config import IS_DEV_MODE
import datetime
import logging 


base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "..", "assets", "grid_layout.json")

# === Grundeinstellungen ===
CELL_SIZE = 60
GRID_WIDTH = 11
GRID_HEIGHT = 10
FONT_SIZE = 48
MARGIN = 10

# Farben
COLOR_BASE = (100, 100, 100)
COLOR_TARGET = (255, 255, 255)
heart_mode_active = False
heart_mode_end_time = None
HEART_ACTIVE = (255, 100, 100)
HEART_INACTIVE = (255, 202, 202)
BG_COLOR = (0, 0, 0)
FADE_SPEED = 3 

# === Grid-Daten laden ===
with open(file_path, encoding="utf-8") as f:
    data = json.load(f)
    grid = data["grid"]
    words = data["words"]

def get_ascii_grid(grid, active_positions):
    lines = []
    for row in range(len(grid)):
        line = ""
        for col in range(len(grid[row])):
            char = grid[row][col]
            if (row, col) in active_positions:
                line += char.upper() + " "
            else:
                line += char.lower() + " "
        lines.append(line)
    return "\n".join(lines)

def get_active_positions(active_words):
    active_positions = set()
    for word in active_words:
        for pos in words.get(word, []):
            active_positions.add(tuple(pos))
    return active_positions

def start_display():
    
    import pygame
    import threading
    
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/clock_output.log",
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="[%H:%M:%S]"
    )

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

            now = datetime.datetime.now()
            if now.minute != current_minute:
                now_rounded = get_current_time()
                active_words = map_time_to_words(now_rounded.hour, now_rounded.minute)
                active_positions = get_active_positions(active_words)
                current_minute = now.minute
                ascii = get_ascii_grid(grid, active_positions)
                text_words = " ".join(active_words)
                logging.info(f"Neue Anzeige: {text_words}\n{ascii}\n")

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

def activate_heart_mode():
    global heart_mode_active, heart_mode_end_time
    heart_mode_active = True
    heart_mode_end_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    print("[DISPLAY] Herz-Modus aktiviert für 1 Stunde.")


if __name__ == "__main__":
    start_display()