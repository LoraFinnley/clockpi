import os
import subprocess
import time
import socket

def is_connected():
    """Prüft, ob eine aktive Internetverbindung besteht."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def start_access_point():
    """Startet hostapd und dnsmasq, um Access Point zu aktivieren."""
    print("[WIFI_MANAGER] Keine Verbindung erkannt. Starte Access Point Modus...")

    # Konfigurationen anpassen falls nötig (hier minimalistisch angenommen)
    subprocess.run(["sudo", "systemctl", "start", "hostapd"])
    subprocess.run(["sudo", "systemctl", "start", "dnsmasq"])

    # Option: eigene IP setzen falls nötig
    subprocess.run(["sudo", "ifconfig", "wlan0", "192.168.4.1"])

    print("[WIFI_MANAGER] Access Point ClockPi-Setup aktiv.")

def stop_access_point():
    """Stoppt hostapd und dnsmasq (z.B. nach erfolgreichem WLAN-Verbinden)."""
    print("[WIFI_MANAGER] Beende Access Point Modus...")
    subprocess.run(["sudo", "systemctl", "stop", "hostapd"])
    subprocess.run(["sudo", "systemctl", "stop", "dnsmasq"])

def connect_to_wifi(ssid, password):
    """WLAN-Konfiguration speichern und Pi neu starten."""
    print(f"[WIFI_MANAGER] Speichere neues WLAN: {ssid}")
    wpa_conf = f"""
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=CH

network={{
    ssid=\"{ssid}\"
    psk=\"{password}\"
}}
"""
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
        f.write(wpa_conf)

    print("[WIFI_MANAGER] WLAN gespeichert. Reboote jetzt...")
    time.sleep(3)
    subprocess.run(["sudo", "reboot"])

def check_and_setup_wifi():
    """Beim Start: prüft Verbindung, startet Access Point falls nötig."""
    if not is_connected():
        start_access_point()
    else:
        print("[WIFI_MANAGER] WLAN Verbindung OK.")
