import os
import time
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Le robot AeroCash est en ligne !"

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def scanner_vols():
    print("🚀 Démarrage du scan AeroCash...")
    while True:
        try:
            print("✈️ Analyse du ciel en cours...")
            time.sleep(600)
        except Exception as e:
            print(f"Erreur : {e}")
            time.sleep(60)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    scanner_vols()
    
