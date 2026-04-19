def scanner_mondial():
    print("🌍 Activation du Radar Mondial AeroCash...")
    envoyer_alerte("🌎 Mode GLOBAL activé ! Je surveille désormais l'ensemble du trafic aérien mondial.")
    
    last_check = 0
    while True:
        try:
            # On interroge l'API pour TOUS les états de vols actuels dans le monde
            url_api = "https://opensky-network.org/api/states/all"
            response = requests.get(url_api, timeout=20)
            
            if response.status_code == 200:
                data = response.json().get('states', [])
                total_vols = len(data) if data else 0
                
                # On ne t'envoie un message que si le nombre de vols change de façon importante
                # ou toutes les 6 heures pour ne pas bloquer ton Telegram
                if time.time() - last_check > 21600: 
                    envoyer_alerte(f"📊 Rapport Mondial : {total_vols} avions sont actuellement en l'air sur la planète. Tout fonctionne !")
                    last_check = time.time()
            
            # Pause pour ne pas se faire bannir par l'API (très important en mode mondial)
            time.sleep(30) 
            
        except Exception as e:
            print(f"Erreur radar : {e}")
            time.sleep(60)
