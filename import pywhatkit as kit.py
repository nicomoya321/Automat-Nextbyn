import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

contacto = "macky"
mensaje = "Mensaje automático 🚀"
driver_path = r"C:\Users\nmoya\Desktop\STOCK\.vscode\msedgedriver.exe"

options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument("--start-maximized")

# IMPORTANTE: usar tu perfil real de Edge
options.add_argument(
    r"user-data-dir=C:\Users\nmoya\AppData\Local\Microsoft\Edge\User Data"
)

service = Service(driver_path)
driver = webdriver.Edge(service=service, options=options)

driver.get("https://web.whatsapp.com")

wait = WebDriverWait(driver, 60)

try:
    print("Esperando que cargue WhatsApp...")

    # Esperar barra de búsqueda
    search_box = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@role="textbox"]'))
    )

    search_box.click()
    search_box.clear()
    search_box.send_keys(contacto)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)

    print("Chat abierto")

    # Esperar caja de mensaje
    message_box = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//footer//div[@contenteditable="true"]'))
    )

    message_box.click()
    time.sleep(1)

    message_box.send_keys(mensaje)
    message_box.send_keys(Keys.ENTER)

    print("✅ Mensaje enviado correctamente")

except Exception as e:
    print("❌ Error:", e)
    input("Revisá el navegador y presioná ENTER para cerrar...")

finally:
    driver.quit()