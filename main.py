import os
import requests
import time
import random

# 1. CARGA DE SECRETOS (Desde la configuración de GitHub)
ltoken = os.environ.get("LTOKEN")
ltuid = os.environ.get("LTUID")

# ID del evento de Genshin Impact (Sacado de tu link)
ACT_ID = "e202102251931481" 

# URLs oficiales de Hoyoverse
url_info = f"https://sg-public-api.hoyolab.com/event/luna/os/info?lang=es-es&act_id={ACT_ID}"
url_sign = f"https://sg-public-api.hoyolab.com/event/luna/os/sign?lang=es-es&act_id={ACT_ID}"

# Cabeceras para simular ser un navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Cookie": f"ltoken_v2={ltoken}; ltuid_v2={ltuid};",
    "Origin": "https://act.hoyolab.com",
    "Referer": "https://act.hoyolab.com/"
}

def main():
    # --- PASO 1: VERIFICAR SI YA COBRASTE ---
    try:
        print(f"🔍 Conectando con Hoyolab para el usuario {ltuid}...")
        resp = requests.get(url_info, headers=headers)
        data = resp.json()
        
        # Si el servidor responde algo raro
        if data["retcode"] != 0:
            print(f"❌ Error al obtener información: {data['message']}")
            return

        # Si ya cobraste hoy, nos detenemos
        if data["data"]["is_sign"]:
            print("✅ ¡Misión cumplida! Ya habías cobrado hoy. No hago nada.")
            return
        
    except Exception as e:
        print(f"⚠️ Error de conexión: {e}")
        return

    # --- PASO 2: ALEATORIEDAD (Para parecer humano) ---
    # Tiramos un dado del 1 al 100
    chance = random.randint(1, 100)
    print(f"🎲 El dado de la suerte sacó: {chance}")
    
    # Si sale mayor a 50, esperamos a la próxima hora (50% de probabilidad de espera)
    # NOTA: GitHub ejecutará esto cada hora. Eventualmente el dado saldrá menor a 50.
    if chance > 50:
        print("⏸️ Decisión: Esperaré a la siguiente hora para que sea más aleatorio.")
        return 

    # --- PASO 3: COBRAR LA RECOMPENSA ---
    print("🚀 Ejecutando cobro de recompensa...")
    
    # Esperamos unos segundos falsos antes de enviar el clic
    time.sleep(random.randint(2, 5)) 
    
    response = requests.post(url_sign, headers=headers)
    result = response.json()
    
    if result["retcode"] == 0:
        print("🎉 ¡ÉXITO! Recompensa reclamada correctamente.")
    else:
        print(f"⚠️ Ocurrió un problema al reclamar: {result['message']}")

if __name__ == "__main__":
    main()