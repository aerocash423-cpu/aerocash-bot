import requests
import time
from datetime import datetime

# --- CONFIGURATION PERSONNELLE ---
USER_OS = "aerocash423-cpu"
PASS_OS = "Ablochampion1643@"

# Ton identifiant récupéré sur l'image
MON_ID = "AeroCash2000" 
# Lien de base AirHelp avec ton ID
MON_LIEN_AIRHELP = f"https://www.airhelp.com/fr/?aid={MON_ID}" 

def detecter_opportunites():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🤖 Analyse AeroCash en cours...")
    url = "https://opensky-network.org/api/states/all"
    
    try:
        r = requests.get(url, auth=(USER_OS, PASS_OS), timeout=15)
        if r.status_code == 200:
            data = r.json()
            states = data.get('states', [])
            
            # Compagnies qui paient bien les indemnités
            compagnies_cibles = ['AFR', 'BAW', 'DLH', 'TAP', 'RAM', 'THY']
            
            for flight in states:
                callsign = flight[1].strip()
                for prefix in compagnies_cibles:
                    if callsign.startswith(prefix):
                        # Génération du lien magique
                        lien_final = f"{MON_LIEN_AIRHELP}&flight_number={callsign}"
                        print(f"💰 OPPORTUNITÉ : Vol {callsign}")
                        print(f"🔗 Lien à partager : {lien_final}")
        else:
            print(f"⚠️ Erreur radar ({r.status_code})")
    except Exception as e:
        print(f"❌ Erreur technique : {e}")

if __name__ == "__main__":
    print("🚀 Robot AeroCash V1.0 - ACTIVÉ")
    while True:
        detecter_opportunites()
        time.sleep(600) # Scan toutes les 10 minutes
