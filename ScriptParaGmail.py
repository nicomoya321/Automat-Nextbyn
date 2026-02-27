import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

smtp_server = "smtp.gmail.com"
smtp_port = 587

email_remitente = "nmoya@nextbyn.com"
password = "dzhecwwqddbhtiyl"  # <-- tu App Password de Gmail

def enviar_correo(destinatario, asunto, cuerpo):

    mensaje = MIMEMultipart("related")
    mensaje["From"] = email_remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto

    msg_alternative = MIMEMultipart("alternative")
    mensaje.attach(msg_alternative)

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size:14px;">

    <p>{cuerpo}</p>
    <br>

    <table cellpadding="0" cellspacing="0" style="border-top:1px solid #ccc; padding-top:10px;">
        <tr>
            <td style="padding-right:15px;">
                <img src="cid:logo_nextbyn" width="120">
            </td>

            <td style="border-left:2px solid #f58220; padding-left:15px;">
                <b style="font-size:16px;">Nicolas Moya</b><br>
                Help Desk Representative<br><br>

                <b>Nextbyn</b><br>
                Av. Carballo 183, Edificio Rivera, Piso 3, Oficina 1<br>
                Rosario, Argentina<br><br>

                📧 soporte@nextbyn.com<br>
                📞 +54 11 5273 40<br>
                🌐 www.nextbyn.com
            </td>
        </tr>
    </table>

    </body>
    </html>
    """

    msg_alternative.attach(MIMEText(html, "html"))

    # 🔥 RUTA AUTOMÁTICA DEL LOGO (SOLUCIÓN DEFINITIVA)
    ruta_logo = os.path.join(os.path.dirname(__file__), "logo.png")
    print("Buscando logo en:", ruta_logo)

    with open(ruta_logo, "rb") as img:
        mime_image = MIMEImage(img.read())
        mime_image.add_header("Content-ID", "<logo_nextbyn>")
        mensaje.attach(mime_image)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_remitente, password)
        server.send_message(mensaje)

    print("✅ Correo enviado con firma")


# -------- EJECUCIÓN --------

destinatario = input("Destinatario: ")
asunto = input("Asunto: ")
cuerpo = input("Mensaje: ")

enviar_correo(destinatario, asunto, cuerpo)