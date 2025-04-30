import threading

from clockpi.utils import wifi_manager
from clockpi.utils import setup_server
from clockpi.ui.display import start_display
from clockpi.telegram.telegram_bot import start_bot


def main():
    print("[MAIN] ClockPi startet...")

    wifi_manager.check_and_setup_wifi()

    threading.Thread(target=setup_server.start_setup_server, daemon=True).start()
    threading.Thread(target=start_bot, daemon=True).start()

    start_display()

if __name__ == "__main__":
    main()
