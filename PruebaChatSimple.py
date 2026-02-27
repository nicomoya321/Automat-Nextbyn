import pywhatkit as kit
import webbrowser
import time
import os

# Ruta de Microsoft Edge
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Verificar que exista
if not os.path.exists(edge_path):
    print("❌ No se encontró Microsoft Edge en la ruta especificada.")
    exit()

# Registrar Edge como navegador manual
webbrowser.register(
    'edge',
    None,
    webbrowser.BackgroundBrowser(edge_path)
)

numero = "+54 9 3412 84-6062"
mensaje = "Bien bro , debe estar trabajando supongo"

try:
    print("Abriendo WhatsApp Web en Microsoft Edge...")

    # Abrir WhatsApp Web en Edge
    webbrowser.get('edge').open("https://web.whatsapp.com")

    time.sleep(10)  # Esperar carga inicial

    # Enviar mensaje
    kit.sendwhatmsg_instantly(
        numero,
        mensaje,
        wait_time=20,
        tab_close=False  # No cerrar pestaña (más estable)
    )

    print("✅ Mensaje enviado correctamente")

except Exception as e:
    print("❌ Error:", e)