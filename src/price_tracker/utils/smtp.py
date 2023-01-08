import smtplib, ssl


def main():

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "aitormarseras95@gmail.com"  # Enter your address
    receiver_email = "aitormarseras95@gmail.com"  # Enter receiver address
    password = input("Type your password and press enter: ")
    message = """\
    Subject: Hi there

    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def main2():
    import smtplib, ssl

    smtp_server = "localhost"
    port = 1025  # For starttls
    sender_email = "my@gmail.com"

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        #server.login(sender_email)
        server.sendmail()
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()


if __name__ == "__main__":
    main()
