import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask('')

# --- RÉCUPÉRATION SÉCURISÉE DEPUIS LE COFFRE-FORT RENDER ---
TOKEN_TELEGRAM = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

@app.route('/')
def home():
    return "🚀 AeroCash Engine v1.0 - Radar Sécurisé et Actif"

def envoyer_alerte(message):
    if not TOKEN_TELEGRAM or not CHAT_ID:
        print("Erreur : Variables d'environnement manquantes sur Render")
        return
        
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage?chat_id={CHAT_ID}&text={message}"
    try:
        requests.get(url, timeout=10)
    except Exception as e:
        print(f"Erreur envoi : {e}")

def scanner_vols_abidjan():
    print("🛰️ Radar AeroCash en mode surveillance sécurisée...")
    # Petit message pour confirmer que le coffre-fort fonctionne
    envoyer_alerte("🔐 Système sécurisé ! Les clés sont maintenant protégées dans le coffre-fort. Surveillance en cours.")
    
    while True:
        try:
            # Simulation du scan de l'API aérienne
            url_api = "https://opensky-network.org/api/states/all"
            response = requests.get(url_api, timeout=15)
            
            if response.status_code == 200:
                data = response.json().get('states', [])
                nb_vols = len(data) if data else 0
                print(f"🔎 Scan effectué : {nb_vols} vols détectés.")
            
            # Rapport toutes les 4 heures
            time.sleep(14400) 
            
        except Exception as e:
            time.sleep(300)

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    scanner_vols_abidjan()
