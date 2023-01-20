import configparser
import smtplib
import ssl
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

import tomli

from constants import SMTP_CFG_PATH, LOGS_PATH


def send_logs_via_email(today: str, logs_path: Path):
    SMTP_CFG = load_smtp_settings(SMTP_CFG_PATH)

    # Load desired logs
    with open(logs_path, mode='r') as f:
        body = f.read()

    # em = EmailMessage()
    # em['From'] = SMTP_CFG['sender_email']
    # em['To'] = SMTP_CFG['receiver_emails']
    # em['subject'] = f'Logs dia {today.replace("_", "-")}'
    # em.set_content(body)
    # for receiver in SMTP_CFG['receiver_emails']:

    em = MIMEMultipart()
    em['From'] = SMTP_CFG['sender_email']
    em['To'] = ','.join(SMTP_CFG['receiver_emails'])
    em['Subject'] = f'Logs dia {today.replace("_", "-")}'
    body_part = MIMEText(body, 'plain')
    em.attach(body_part)

    with open(r"C:\Users\110414\PycharmProjects\Seguidor-de-precios\src\price_tracker\outputs\01_listado_precios_Enero.xlsx", 'rb') as file:
        # Attach the file with filename to the email
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(file.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % 'prueba.xlsx')
        em.attach(p)
        # em.attach(MIMEApplication(file.read(), Name=f'prueba.xlsx'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_CFG['smtp_server'], SMTP_CFG['port'], context=context) as server:
        server.login(SMTP_CFG['sender_email'], SMTP_CFG['password'])
        server.sendmail(SMTP_CFG['sender_email'], SMTP_CFG['receiver_emails'], em.as_string())


def load_smtp_settings(path: Path):
    if path.suffix == '.cfg':
        config = configparser.ConfigParser()
        with open(path) as f:
            config.read_file(f)
            config_dict = {
                "port": config.get('sender settings', 'port'),
                "smtp_server": config.get('sender settings', 'smtp_server'),
                "sender_email": config.get('sender settings', 'email'),
                "password": config.get('sender settings', 'password'),
                "receiver_emails": config.get('receiver settings', 'emails'),
            }
            # port = config.get('sender settings', 'port')
            # smtp_server = config.get('sender settings', 'smtp_server')
            # sender_email = config.get('sender settings', 'email')
            # password = config.get('sender settings', 'password')
            # receiver_emails = config.get('receiver settings', 'email')

    elif path.suffix == '.toml':
        with open(path, mode="rb") as fp:
            config_dict = tomli.load(fp)

    return config_dict


if __name__ == "__main__":
    print(load_smtp_settings(SMTP_CFG_PATH))
    # from datetime import datetime
    # today_datetime = datetime.now().date()
    # today = today_datetime.isoformat().replace("-", "_")
    today = "2023_01_10"
    print(f'Sending warning logs of {today} via email')
    send_logs_via_email(today, LOGS_PATH / f'{today}_warnings.log')
    print(f'Logs sent, exiting program!')

