import requests
import time
import pandas as pd
from datetime import datetime

# ================= CONFIGURACIÓN =================
WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/w1UkhsAAAAE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=c7nTLVJLxKNiI4dZMVJJOjzO9U2q4HWzgcahZRvl-x0"
HORA_ENVIO = "11:47"  # HH:MM (24 hs)
EXCEL_PATH = r"C:\Users\nmoya\Desktop\STOCK\.vscode\estadoTK1.xls"

ESTADOS_FILTRADOS = ["abierto", "contactado"]
ORDEN_ESTADOS = ["abierto", "contactado"]

# ================= FUNCIONES AUXILIARES =================
def calcular_proximo_envio():
    ahora = datetime.now()
    hora_objetivo = datetime.strptime(HORA_ENVIO, "%H:%M").time()
    envio = datetime.combine(ahora.date(), hora_objetivo)

    if ahora >= envio:
        envio += pd.Timedelta(days=1)

    return envio


# ================= FUNCIONES PRINCIPALES =================
def tickets_actuales():
    df = pd.read_excel(EXCEL_PATH)
    
    # Filtrar por estados
    df_activos = df[df['estado'].str.lower().isin(ESTADOS_FILTRADOS)]
    
    # Obtener operadores únicos
    operadores_totales = df['propietario'].unique().tolist()
    
    return df_activos, operadores_totales, 'propietario'


def enviar_mensaje():
    df_activos, operadores_totales, columna_propietario = tickets_actuales()

    operadores_sin_tickets = []

    for operador in operadores_totales:
        df_operador = df_activos[df_activos[columna_propietario] == operador]

        if df_operador.empty:
            operadores_sin_tickets.append(operador)

    if not operadores_sin_tickets:
        mensaje_texto = "✅ Todos los operadores tienen tickets activos (Abierto / Contactado)."
    else:
        mensaje_texto = "📌 Operadores sin tickets activos (Abierto / Contactado):\n\n"

        for operador in operadores_sin_tickets:
            mensaje_texto += f"🙍 {operador} está sin tickets activos\n"

    response = requests.post(WEBHOOK_URL, json={"text": mensaje_texto})

    if response.status_code == 200:
        print("Mensaje enviado correctamente")
    else:
        print("Error al enviar mensaje:", response.text)


# ================= ENVÍO MENSAJE =================
def enviar_mensaje():
    df_activos, operadores_totales, columna_propietario = tickets_actuales()

    operadores_sin_tickets = []

    for operador in operadores_totales:
        df_operador = df_activos[df_activos[columna_propietario] == operador]

        if df_operador.empty:
            operadores_sin_tickets.append(operador)

    # Si nadie tiene tickets
    if not operadores_sin_tickets:
        mensaje_texto = "✅ Todos los operadores tienen tickets asignados."
    else:
        mensaje_texto = "📌 Operadores SIN tickets activos:\n\n"

        for operador in operadores_sin_tickets:
            mensaje_texto += f"🙍 {operador}\n"

    # Enviar mensaje
    response = requests.post(WEBHOOK_URL, json={"text": mensaje_texto})

    if response.status_code == 200:
        print("Mensaje enviado correctamente")
    else:
        print("Error al enviar mensaje:", response.text)


# ================= LOOP PRINCIPAL =================
print("Bot tickets activos iniciado")

while True:
    proximo_envio = calcular_proximo_envio()
    segundos = (proximo_envio - datetime.now()).total_seconds()

    print(f"Próximo envío: {proximo_envio}")
    time.sleep(max(0, segundos))

    enviar_mensaje()
    time.sleep(60)