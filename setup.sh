echo "Update Paketquellen..."
sudo apt update

echo "Installiere Systempakete..."
sudo apt install -y hostapd dnsmasq

echo "Installiere Python-Pakete..."
pip install -r requirements.txt

echo "Deaktiviere automatische Services (werden manuell gestartet)..."
sudo systemctl disable hostapd
sudo systemctl disable dnsmasq

echo "Fertig! Raspberry Pi ist bereit."
