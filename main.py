import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask('')

# --- TA CONFIGURATION FINALE ---
TOKEN_TELEGRAM = "8600657255:AAHdyDgWxecU7a7Uq1605CrkQ1sr2KBgV1k"
# Remplace 123456789 par ton ID récupéré avec @userinfobot
CHAT_ID = "TON_ID_USERINFOBOT" 

@app.route('/')
def home():
    return "🚀 AeroCash Engine v1.0 - Surveillance Active"

def envoyer_alerte(message):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage?chat_id={CHAT_ID}&text={message}"
    try:
        requests.get(url)
    except:
        pass

def scanner_vols():
    print("🛰️ Surveillance du ciel activée...")
    # Premier message pour te dire que c'est prêt
    envoyer_alerte("✅ Salut Ablo ! Ton robot AeroCash est maintenant opérationnel. Je surveille les retards pour toi.")
    
    while True:
        try:
            # Simulation d'un scan de retard vers Abidjan (ABJ)
            print("🔎 Scan des vols vers ABJ...")
            # Ici on pourra ajouter l'API OpenSky demain si tu veux plus de détails
            time.sleep(3600) # On scanne toutes les heures
        except Exception as e:
            time.sleep(60)

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    scanner_vols()
