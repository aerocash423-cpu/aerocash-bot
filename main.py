import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask('')

TOKEN_TELEGRAM = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

@app.route('/')
def home():
    return "🌍 AeroCash Radar : Axe Afrique-Europe Actif"

def envoyer_alerte(message):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage?chat_id={CHAT_ID}&text={message}"
    try:
        requests.get(url, timeout=10)
    except:
        pass

def scanner_afrique_europe():
    print("📡 Surveillance de l'axe Afrique-Europe lancée...")
    envoyer_alerte("🚀 Radar AeroCash v2.0 : Surveillance AFRIQUE & EUROPE activée. Je scanne les vols intercontinentaux.")
    
    while True:
        try:
            # Coordonnées pour couvrir l'Afrique et l'Europe (Latitude/Longitude)
            # Cette zone va du sud de l'Afrique jusqu'au nord de la Norvège
            params = {
                "lamin": -35.0, # Sud (Afrique du Sud)
                "lamin_max": 70.0, # Nord (Europe)
                "lomin": -25.0, # Ouest (Atlantique/Sénégal)
                "lomax": 55.0   # Est (Moyen-Orient/Est Afrique)
            }
            
            url_api = "https://opensky-network.org/api/states/all"
            response = requests.get(url_api, params=params, timeout=20)
            
            if response.status_code == 200:
                data = response.json().get('states', [])
                nb_vols = len(data) if data else 0
                print(f"🔎 Scan zone : {nb_vols} vols en cours.")
                
                # Petit rapport toutes les 6 heures pour confirmer la vigilance
                # On pourra ajouter des filtres de retard demain
                envoyer_alerte(f"📊 Rapport Zone : {nb_vols} vols détectés sur l'axe Afrique-Europe. Surveillance continue.")
            
            # Pause de 6 heures pour rester discret et efficace
            time.sleep(21600)
            
        except Exception as e:
            print(f"Erreur : {e}")
            time.sleep(300)

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    scanner_afrique_europe()
