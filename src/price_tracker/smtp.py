import configparser
import smtplib
import ssl
from pathlib import Path
from email.message import EmailMessage

from constants import SMTP_CFG_PATH, LOGS_PATH


def send_logs_via_email(today: str, logs_path: Path):
    SMTP_CFG = load_smtp_settings(SMTP_CFG_PATH)

    # Load desired logs
    with open(logs_path, mode='r') as f:
        body = f.read()

    em = EmailMessage()
    em['From'] = SMTP_CFG['sender_email']
    em['To'] = SMTP_CFG['receiver_email']
    em['subject'] = f'Logs dia {today.replace("_", "-")}'
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_CFG['smtp_server'], SMTP_CFG['port'], context=context) as server:
        server.login(SMTP_CFG['sender_email'], SMTP_CFG['password'])
        server.sendmail(SMTP_CFG['sender_email'], SMTP_CFG['receiver_email'], em.as_string())


def load_smtp_settings(path: Path):
    config = configparser.ConfigParser()
    with open(path) as f:
        config.read_file(f)
        config_dict = {
            "port": config.get('sender settings', 'port'),
            "smtp_server": config.get('sender settings', 'smtp_server'),
            "sender_email": config.get('sender settings', 'email'),
            "password": config.get('sender settings', 'password'),
            "receiver_email": config.get('receiver settings', 'email'),
        }
        # port = config.get('sender settings', 'port')
        # smtp_server = config.get('sender settings', 'smtp_server')
        # sender_email = config.get('sender settings', 'email')
        # password = config.get('sender settings', 'password')
        # receiver_email = config.get('receiver settings', 'email')
    return config_dict


if __name__ == "__main__":
    from datetime import datetime
    today_datetime = datetime.now().date()
    today = today_datetime.isoformat().replace("-", "_")
    print(f'Sending warning logs of {today} via email')
    send_logs_via_email(today, LOGS_PATH / f'{today}_warnings.log')
    print(f'Logs sent, exiting program!')

