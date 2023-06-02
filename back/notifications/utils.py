import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from settings import config
import requests

sender_email = config['EMAIL']
sender_password = config['PASS']


def download_from_link(link, local_path):
    response = requests.get(link)
    open(local_path, 'wb').write(response.content)

def send_email(recipient_email, subject, message, s3_links=None):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    local_paths = []

    if s3_links is not None:
        for s3_link in s3_links:
            local_path = './temp/' + s3_link.split('/')[-2] + s3_link.split('/')[-1]
            download_from_link(s3_link, local_path)
            local_paths.append(local_path)

        for local_path in local_paths:
            with open(local_path, 'rb') as attachment:
                part = MIMEApplication(attachment.read(), Name=os.path.basename(local_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(local_path)}"'
                msg.attach(part)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

    for local_path in local_paths:
        os.remove(local_path)