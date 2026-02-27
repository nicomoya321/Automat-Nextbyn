import requests
import time
from datetime import datetime, timedelta, date
import pandas as pd  # type: ignore

# ================= CONFIGURACIÓN =================
WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQAY_KDZU4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=zgI7f5A9414MVMhLI4eeJp-0gWEiJ96CoZKOTmZAdGc"
HORA_ENVIO = "23:24"  # HH:MM (24 hs)
EXCEL_PATH = r"C:\Users\nmoya\Desktop\STOCK\.vscode\vencen1.xls"

FERIADOS2026 = [
    "2026-01-01","2026-02-16","2026-02-17","2026-03-24",
    "2026-04-02","2026-04-03","2026-05-01","2026-05-25",
    "2026-06-15","2026-06-20","2026-07-09","2026-08-17",
    "2026-10-12","2026-11-23","2026-12-08","2026-12-25"
]

ESTADOS_FILTRADOS = ["Abierto", "Contactado"]

# ================= FUNCIONES AUXILIARES =================
def es_feriado(fecha: date) -> bool:
    return fecha.strftime("%Y-%m-%d") in FERIADOS2026

def es_fin_de_semana(fecha: date) -> bool:
    return fecha.weekday() >= 5

def calcular_proximo_envio():
    ahora = datetime.now()
    hora_objetivo = datetime.strptime(HORA_ENVIO, "%H:%M").time()
    envio = datetime.combine(ahora.date(), hora_objetivo)

    if ahora >= envio:
        envio += timedelta(days=1)

    return envio

# ================= FUNCIONES PRINCIPALES =================
def tickets_para_manana():
    df = pd.read_excel(EXCEL_PATH)

    # Normalizar nombres de columnas (evita KeyError)
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # 🔎 
    columna_propietario = "propietario"
    columna_fecha_vencimiento = "fecha_de_vencimiento"
    columna_ticket = "ticket"
    columna_estado = "estado"

    # Verificar que existan
    columnas_necesarias = [
        columna_propietario,
        columna_fecha_vencimiento,
        columna_ticket,
        columna_estado
    ]

    for col in columnas_necesarias:
        if col not in df.columns:
            raise ValueError(f"La columna '{col}' no existe en el Excel. Columnas detectadas: {df.columns.tolist()}")

    # ================= CONVERSIÓN SEGURA DE FECHA =================
    df[columna_fecha_vencimiento] = (
        pd.to_datetime(
            df[columna_fecha_vencimiento],
            errors="coerce"
        )
        .dt.normalize()
    )

    # Convertir ticket a string
    df[columna_ticket] = (
    pd.to_numeric(df[columna_ticket], errors="coerce")
    .fillna(0)
    .astype(int)
    .astype(str)
)

    # Limpieza de estado
    df[columna_estado] = (
        df[columna_estado]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df = df[df[columna_estado].isin([e.lower() for e in ESTADOS_FILTRADOS])]

    # Fecha de mañana
    manana = pd.to_datetime(date.today() + timedelta(days=1)).normalize()

    # Filtrar tickets que vencen mañana
    df_manana = df[df[columna_fecha_vencimiento] == manana]

    # Resumen por operador
    resumen_operador = (
        df_manana.groupby(columna_propietario)
        .size()
        .reset_index(name="tickets")
        .sort_values(by=columna_propietario)
    )

    return df_manana, resumen_operador, columna_propietario, columna_ticket

# ================= ENVÍO MENSAJE =================
def enviar_mensaje():
    hoy = date.today()

    if es_fin_de_semana(hoy):
        print("Fin de semana - no se envía mensaje.")
        return

    if es_feriado(hoy):
        print("Feriado - no se envía mensaje.")
        return

    df_manana, resumen_operador, columna_propietario, columna_ticket = tickets_para_manana()

    if df_manana.empty:
        mensaje_texto = "No hay tickets que se vencen mañana con estado Contactado o Abierto."
    else:
        mensaje_texto = "📌 Tickets que se vencen mañana:\n\n"

        for operador in sorted(resumen_operador[columna_propietario]):
            tickets_operador = df_manana[df_manana[columna_propietario] == operador]

            mensaje_texto += f"🙍 {operador} - {len(tickets_operador)} tickets\n"

            for _, row in tickets_operador.iterrows():
                mensaje_texto += f"   🎫 ID: {row[columna_ticket]}\n"

            mensaje_texto += "\n"

    mensaje = {"text": mensaje_texto}
    response = requests.post(WEBHOOK_URL, json=mensaje)

    if response.status_code == 200:
        print("Mensaje enviado correctamente")
    else:
        print("Error al enviar mensaje:", response.text)

# ================= LOOP PRINCIPAL =================
print("Bot Mesa 2 iniciado")

while True:
    proximo_envio = calcular_proximo_envio()
    segundos = (proximo_envio - datetime.now()).total_seconds()

    print(f"Próximo envío: {proximo_envio}")

    time.sleep(max(0, segundos))
    enviar_mensaje()
    time.sleep(60)