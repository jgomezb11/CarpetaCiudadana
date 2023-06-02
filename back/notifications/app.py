from flask import Flask
from settings import config

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

app = Flask(__name__)
app.config.update(config)

def create_app():
    global app
    with app.app_context():
        from routes import user_blueprint
        app.register_blueprint(user_blueprint)
    return app



def send_email(sender_email, sender_password, recipient_email, subject, message, attachment_paths=None):
    # Crear el mensaje de correo
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Agregar el cuerpo del mensaje
    msg.attach(MIMEText(message, 'plain'))

    if attachment_paths is not None:
        for attachment_path in attachment_paths:
            if os.path.exists(attachment_path):
                # Adjuntar el archivo al mensaje
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                    msg.attach(part)
            else:
                print(f"No se encontró el archivo en la ruta especificada: {attachment_path}")


    # Configurar el servidor SMTP y enviar el correo
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

# Ejemplo de uso
sender_email = ''  # Reemplaza con tu dirección de correo electrónico
sender_password = ''  # Reemplaza con tu contraseña de aplicaciones de correo electrónico
recipient_email = ''  # Reemplaza con la dirección de correo del destinatario
subject = 'Asunto del correo'
message = 'Contenido del correo'
attachment_paths = ['','']  # Lista de rutas a los archivos que deseas adjuntar


send_email(sender_email, sender_password, recipient_email, subject, message, attachment_paths)
