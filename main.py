import os
import requests
import time
import random

# --- CONFIGURACIÓN ---
ltoken = os.environ.get("LTOKEN")
ltuid = os.environ.get("LTUID")
cookie_token = os.environ.get("COOKIE_TOKEN") # <--- AQUI ESTA LA MAGIA

# ID del evento de Genshin (Global)
ACT_ID = "e202102251931481" 

url_info = f"https://sg-public-api.hoyolab.com/event/luna/os/info?lang=es-es&act_id={ACT_ID}"
url_sign = f"https://sg-public-api.hoyolab.com/event/luna/os/sign?lang=es-es&act_id={ACT_ID}"

# Construimos la cookie maestra con todas las piezas
# Nota: account_id_v2 suele ser el mismo que ltuid_v2
cookie_str = f"ltoken_v2={ltoken}; ltuid_v2={ltuid}; cookie_token_v2={cookie_token}; account_id_v2={ltuid};"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Cookie": cookie_str,
    "Origin": "https://act.hoyolab.com",
    "Referer": "https://act.hoyolab.com/"
}

def main():
    print(f"🔍 Conectando como usuario: {ltuid}...")

    # 1. VERIFICAR
    try:
        resp = requests.get(url_info, headers=headers)
        data = resp.json()
        
        if data.get("retcode") != 0:
            print(f"❌ Error al leer estado: {data.get('message')}")
            print("👉 Pista: Si dice 'No has iniciado sesión', revisa que copiaste bien el cookie_token")
            return

        if data["data"]["is_sign"]:
            print("✅ Hoy YA has cobrado. ¡Vuelve mañana!")
            return
        
    except Exception as e:
        print(f"⚠️ Error de conexión: {e}")
        return

    # 2. DECIDIR (ALEATORIEDAD)
    # Para probar HOY, forzamos que se ejecute (probabilidad > 0)
    chance = random.randint(1, 100)
    print(f"🎲 Dado: {chance}")
    
    # En producción real, descomenta esto para que a veces espere:
    # if chance > 80: 
    #    print("⏸️ Decisión: Esperaré a la siguiente hora.")
    #    return 

    # 3. COBRAR
    print("🚀 Intentando cobrar recompensa...")
    time.sleep(random.randint(2, 5)) 
    
    response = requests.post(url_sign, headers=headers)
    result = response.json()
    
    # Manejo de respuestas
    if result.get("retcode") == 0:
        print("🎉 ¡ÉXITO! Recompensa reclamada.")
    else:
        print(f"⚠️ Respuesta del servidor: {result.get('message')}")

if __name__ == "__main__":
    main()