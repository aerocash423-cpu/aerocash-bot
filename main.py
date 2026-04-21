import os
import time
import logging
from threading import Thread, Lock

import requests
from flask import Flask, jsonify

app = Flask(__name__)

# -----------------------------
# Configuration
# -----------------------------
TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PORT = int(os.getenv("PORT", "10000"))

SCAN_INTERVAL_SECONDS = int(os.getenv("SCAN_INTERVAL_SECONDS", "21600"))  # 6h
RETRY_DELAY_SECONDS = int(os.getenv("RETRY_DELAY_SECONDS", "300"))        # 5 min
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "20"))
RUN_SCANNER = os.getenv("RUN_SCANNER", "true").lower() == "true"

OPENSKY_URL = "https://opensky-network.org/api/states/all"
BBOX = {
    "lamin": -35.0,
    "lamax": 70.0,
    "lomin": -25.0,
    "lomax": 55.0,
}

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("aerocash-radar")

# -----------------------------
# HTTP session réutilisable
# -----------------------------
session = requests.Session()
session.headers.update({
    "User-Agent": "AeroCash-Radar/2.1"
})

# -----------------------------
# Scanner state
# -----------------------------
scanner_started = False
scanner_lock = Lock()


# -----------------------------
# Routes web
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "service": "AeroCash Radar",
        "status": "ok",
        "zone": "Afrique-Europe"
    }), 200


@app.route("/healthz")
def healthz():
    return jsonify({"status": "healthy"}), 200


# -----------------------------
# Helpers
# -----------------------------
def validate_config():
    missing = []

    if not TOKEN_TELEGRAM:
        missing.append("TELEGRAM_TOKEN")
    if not CHAT_ID:
        missing.append("CHAT_ID")

    if missing:
        raise RuntimeError(
            f"Variables d'environnement manquantes : {', '.join(missing)}"
        )


def envoyer_alerte(message: str) -> bool:
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"

    try:
        response = session.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=10
        )
        response.raise_for_status()
        logger.info("Alerte Telegram envoyée avec succès.")
        return True

    except requests.RequestException:
        logger.exception("Échec d'envoi de l'alerte Telegram.")
        return False


def recuperer_vols_afrique_europe():
    response = session.get(OPENSKY_URL, params=BBOX, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    payload = response.json()
    states = payload.get("states") or []

    return states


def construire_rapport(nb_vols: int, last_count: int | None) -> str:
    if last_count is None:
        variation = "N/A (premier scan)"
    else:
        delta = nb_vols - last_count
        signe = "+" if delta >= 0 else ""
        variation = f"{signe}{delta}"

    heures = max(1, SCAN_INTERVAL_SECONDS // 3600)

    return (
        "📊 AeroCash Radar | Rapport Afrique-Europe\n"
        f"Vols détectés : {nb_vols}\n"
        f"Variation : {variation}\n"
        f"Zone : lat {BBOX['lamin']}→{BBOX['lamax']} | lon {BBOX['lomin']}→{BBOX['lomax']}\n"
        f"Prochain scan : ~{heures}h"
    )


# -----------------------------
# Scanner loop
# -----------------------------
def scanner_afrique_europe():
    logger.info("📡 Surveillance de l'axe Afrique-Europe lancée...")

    envoyer_alerte(
        "🚀 AeroCash Radar v2.1 démarré.\n"
        "Surveillance Afrique-Europe active."
    )

    last_count = None

    while True:
        try:
            states = recuperer_vols_afrique_europe()
            nb_vols = len(states)

            logger.info("Scan terminé | vols détectés=%s", nb_vols)

            message = construire_rapport(nb_vols, last_count)
            envoyer_alerte(message)

            last_count = nb_vols
            time.sleep(SCAN_INTERVAL_SECONDS)

        except requests.RequestException:
            logger.exception("Erreur réseau/API OpenSky.")
            envoyer_alerte(
                "⚠️ AeroCash Radar : erreur temporaire pendant le scan OpenSky.\n"
                "Nouvelle tentative automatique dans 5 minutes."
            )
            time.sleep(RETRY_DELAY_SECONDS)

        except Exception:
            logger.exception("Erreur inattendue dans le scanner.")
            time.sleep(RETRY_DELAY_SECONDS)


def demarrer_scanner():
    global scanner_started

    if not RUN_SCANNER:
        logger.info("Scanner désactivé via RUN_SCANNER=false")
        return

    with scanner_lock:
        if scanner_started:
            logger.info("Scanner déjà lancé, aucun doublon démarré.")
            return

        thread = Thread(
            target=scanner_afrique_europe,
            name="scanner-afrique-europe",
            daemon=True
        )
        thread.start()
        scanner_started = True

        logger.info("Thread scanner démarré.")


# -----------------------------
# Bootstrap
# -----------------------------
try:
    validate_config()
    demarrer_scanner()
except Exception:
    logger.exception("Échec de l'initialisation de l'application.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
    
