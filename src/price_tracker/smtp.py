import smtplib, ssl
from pathlib import Path


def send_logs_via_email():

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "aitormarseras95@gmail.com"  # Enter your address
    receiver_email = "aitormarseras95@gmail.com"  # Enter receiver address

    res_pth = Path('resources/pswd.txt')
    with open(res_pth, mode="r") as f:
        password = f.read()

    message = """\
    Subject: Hi there

    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


if __name__ == "__main__":
    main()

