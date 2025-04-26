from flask import Flask, request, redirect
import threading
import wifi_manager

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html lang='de'>
<head>
    <meta charset='UTF-8'>
    <title>ClockPi WLAN Setup</title>
</head>
<body style='font-family:sans-serif; text-align:center; padding-top:50px;'>
    <h1>ClockPi WLAN Setup</h1>
    <form method='POST'>
        <input name='ssid' type='text' placeholder='WLAN Name (SSID)' required style='padding:10px; width:80%;'><br><br>
        <input name='password' type='password' placeholder='WLAN Passwort' required style='padding:10px; width:80%;'><br><br>
        <button type='submit' style='padding:10px 20px; font-size:16px;'>Verbinden</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def wifi_setup():
    if request.method == 'POST':
        ssid = request.form.get('ssid')
        password = request.form.get('password')
        if ssid and password:
            threading.Thread(target=wifi_manager.connect_to_wifi, args=(ssid, password)).start()
            return "<h2>Verbindung wird hergestellt... Pi startet neu...</h2>"
    return HTML_FORM

def start_setup_server():
    app.run(host='0.0.0.0', port=80)