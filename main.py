import os
import time
from flask import Flask
from threading import Thread

# 1. On crée un mini-site pour rassurer Render
app = Flask('')

@app.route('/')
def home():
    return "Le robot AeroCash est en ligne !"

def run():
    # Render utilise le port 10000 par défaut
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Ton vrai travail de robot
def scanner_vols():
    print("🚀 Démarrage du scan AeroCash...")
    while True:
        try:
            # C'est ici que ton code cherche les avions
            print("✈️ Analyse du ciel en cours pour AeroCash2000...")
            # On simule un travail
            time.sleep(600) # Attend 10 minutes
        except Exception as e:
            print(f"Erreur : {e}")
            time.sleep(60)

# 3. On lance les deux en même temps
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    scanner_vols()
