import requests
import time
from datetime import datetime, timedelta, date

WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAR5wm-pE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=zQdtt_jWFqBF5og5AgCwidoBHI5DPLU4Q6bv9Zw7Z-c"

# ================= CONFIGURACIÓN =================
HORA_ENVIO = "07:02"  # HH:MM (24 hs)

nexty_personas = ["Brau", "Marian", "Nico", "Dai"]
devolucion_personas = ["Dai", "Cin", "Nico", "Marian", "Brau"]

FERIADOS2026 = [
     "2026-01-01",  # Año Nuevo
    "2026-02-16",  # Lunes de Carnaval
    "2026-02-17",  # Martes de Carnaval
    "2026-03-24",  # Día de la Memoria por la Verdad y la Justicia
    "2026-04-02",  # Día del Veterano y de los Caídos en Malvinas (y Jueves Santo)
    "2026-04-03",  # Viernes Santo
    "2026-05-01",  # Día del Trabajador
    "2026-05-25",  # Día de la Revolución de Mayo
    "2026-06-15",  # Paso a la Inmortalidad de Martín Miguel de Güemes
    "2026-06-20",  # Día de la Bandera – Manuel Belgrano
    "2026-07-09",  # Día de la Independencia
    "2026-08-17",  # Paso a la Inmortalidad de José de San Martín
    "2026-10-12",  # Día del Respeto a la Diversidad Cultural
    "2026-11-23",  # Día de la Soberanía Nacional
    "2026-12-08",  # Inmaculada Concepción
    "2026-12-25",  # Navidad
]
# =================================================

def es_feriado(fecha: date) -> bool:
    return fecha.strftime("%Y-%m-%d") in FERIADOS2026

def es_fin_de_semana(fecha: date) -> bool:
    return fecha.weekday() >= 5  # sábado o domingo

def calcular_proximo_envio():
    ahora = datetime.now()
    hora_objetivo = datetime.strptime(HORA_ENVIO, "%H:%M").time()
    envio = datetime.combine(ahora.date(), hora_objetivo)

    if ahora >= envio:
        envio += timedelta(days=1)

    return envio

def rotar(lista, dias):
    return lista[dias % len(lista):] + lista[:dias % len(lista)]

def enviar_mensaje():
    hoy = date.today()

    if es_fin_de_semana(hoy):
        print(f"📆 Hoy {hoy} es fin de semana. No se envía mensaje.")
        return

    if es_feriado(hoy):
        print(f"📅 Hoy {hoy} es feriado. No se envía mensaje.")
        return

    dias = (hoy - date(2024, 1, 1)).days

    nexty = rotar(nexty_personas, dias)
    devolucion = rotar(devolucion_personas, dias)

    mensaje = {
        "text": (
            "📋 *Diagrama de atención para hoy de Mesa 2*\n\n"
            "Nexty.\n\n"
            f"08 a 09 {nexty[0]}\n"
            f"09 a 10 {nexty[1]}\n"
            f"13 a 14 {nexty[2]}\n\n"
            "Devolución de llamadas\n\n"
            f"08 a 09 {devolucion[0]}\n"
            f"09 a 10 {devolucion[1]}\n"
            f"13 a 14 {devolucion[2]}"
        )
    }

    response = requests.post(WEBHOOK_URL, json=mensaje)

    if response.status_code == 200:
        print("✅ Mensaje enviado correctamente")
    else:
        print("❌ Error al enviar mensaje:", response.text)

# ================= LOOP PRINCIPAL =================
print("🤖 Bot Mesa 2 iniciado")

while True:
    proximo_envio = calcular_proximo_envio()
    segundos = (proximo_envio - datetime.now()).total_seconds()

    print(f"⏳ Próximo envío: {proximo_envio}")
    time.sleep(max(0, segundos))

    enviar_mensaje()

    # Espera corta para evitar doble ejecución
    time.sleep(60)
