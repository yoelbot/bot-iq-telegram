from iqoptionapi.stable_api import IQ_Option
from telegram import Bot
import time
import logging

# === Tus datos ===
EMAIL = 'yoelaguilar27.ya@outlook.com'        # ✅ Tu correo de IQ Option
PASSWORD = 'Aguilar27'            # ✅ Tu contraseña IQ Option
TOKEN_TELEGRAM = '8250445329:AAEoEqJg8oGoFPFzKvs0wXpsh-2dCe4fm2Q'  # ✅ Tu token de Telegram
CHAT_ID = 562640811                           # ✅ Tu ID de chat
TIEMPO_ESPERA = 60                             # Tiempo de espera entre escaneos

# === Inicializar IQ Option ===
I_want_money = IQ_Option(EMAIL, PASSWORD)
I_want_money.connect()

# === Inicializar Telegram ===
bot = Bot(token=TOKEN_TELEGRAM)

# === Pares a analizar ===
pares = ["EURUSD-OTC", "EURGBP-OTC"]

# === Función para obtener velas ===
def obtener_velas(par):
    try:
        velas = I_want_money.get_candles(par, 60, 3, time.time())
        return velas
    except:
        return None

# === Lógica básica de análisis de señal ===
def analizar_senal(velas):
    vela1, vela2, vela3 = velas
    if vela1['close'] < vela1['open'] and vela2['close'] < vela2['open'] and vela3['close'] > vela3['open']:
        return "CALL"
    elif vela1['close'] > vela1['open'] and vela2['close'] > vela2['open'] and vela3['close'] < vela3['open']:
        return "PUT"
    else:
        return None

# === Confirmación de conexión inicial ===
if I_want_money.check_connect():
    print("[IQ ✅] Conectado correctamente")
    bot.send_message(chat_id=CHAT_ID, text="🤖 Bot conectado a IQ Option correctamente")
else:
    print("[IQ ❌] Error de conexión")
    exit()

# === Bucle principal ===
while True:
    print("⏳ Iniciando escaneo de señales...")
    for par in pares:
        try:
            velas = obtener_velas(par)
            if velas:
                señal = analizar_senal(velas)
                if señal:
                    mensaje = f"[📢] Señal en {par}: {señal}"
                    print(mensaje)
                    bot.send_message(chat_id=CHAT_ID, text=mensaje)
                else:
                    print(f"❌ Sin señal en {par}")
            else:
                print(f"[⚠️] No se pudieron obtener velas de {par}, reintentando...")
        except Exception as e:
            print(f"[⚠️] Error en {par}. Intentando reconectar...")
            I_want_money.connect()
            time.sleep(2)
        time.sleep(1)
    
    print(f"⏳ Esperando {TIEMPO_ESPERA} segundos para nuevo escaneo...\n")
    time.sleep(TIEMPO_ESPERA)
