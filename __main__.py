import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import wifi_manager
from utils import setup_server
from ui.display import start_display
from telegram.bot import start_bot_in_thread

def main():
    print("[MAIN] ClockPi startet...")

    wifi_manager.check_and_setup_wifi()

    start_bot_in_thread()

    threading.Thread(target=setup_server.start_setup_server, daemon=True).start()

    start_display()

if __name__ == "__main__":
    main()
