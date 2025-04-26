# ui/terminal_display.py
import time
import os
import json

from clock.time_manager import get_current_time
from clock.word_mapper import map_time_to_words

CELL_SIZE = 2  # Einfachheit: 2 Leerzeichen Abstand
REFRESH_RATE = 1  # Sekunden

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_terminal_display():
    with open(os.path.join("assets", "grid_layout.json"), encoding="utf-8") as f:
        data = json.load(f)
        grid = data["grid"]
        words = data["words"]

    while True:
        now = get_current_time()
        active_words = map_time_to_words(now.hour, now.minute)

        active_positions = set()
        for word in active_words:
            active_positions.update(tuple(pos) for pos in words.get(word, []))

        clear_terminal()
        print("\nClockPi - Terminal Modus\n")
        for row in range(len(grid)):
            line = ""
            for col in range(len(grid[row])):
                char = grid[row][col]
                if (row, col) in active_positions:
                    line += f"\033[1m{char}\033[0m "  # Fettdruck (hell)
                else:
                    line += f"{char.lower()} "  # Normal (klein)
            print(line)

        time.sleep(REFRESH_RATE)