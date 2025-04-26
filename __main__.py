# __main__.py
import threading
import wifi_manager
import setup_server
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
