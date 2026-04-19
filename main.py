
import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask('')

# --- TA CONFIGURATION FINALE ---
TOKEN_TELEGRAM = "8600657255:AAHdyDgWxecU7a7Uq1605CrkQ1sr2KBgV1k"
CHAT_ID = "6800954750" 

@app.route('/')
def home():
    return "🚀 AeroCash Engine v1.0 est en ligne et surveille le ciel !"

def envoyer_alerte(message):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage?chat_id={CHAT_ID}&text={message}"
    try:
        requests.get(url, timeout=10)
    except:
        pass

def scanner_vols():
    print("🛰️ Surveillance AeroCash activée...")
    # Le robot te prévient dès qu'il démarre
    envoyer_alerte("🚀 Félicitations Ablo ! Ton robot AeroCash est officiellement actif. Je commence la surveillance des vols vers Abidjan.")
    
    while True:
        try:
            # Pour l'instant on simule le scan pour vérifier que la liaison marche
            print("🔎 Scan des retards en cours...")
            
            # Message de test toutes les 3 heures pour ne pas te déranger
            # On pourra affiner la détection réelle demain
            time.sleep(10800) 
        except Exception as e:
            time.sleep(60)

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    scanner_vols()
