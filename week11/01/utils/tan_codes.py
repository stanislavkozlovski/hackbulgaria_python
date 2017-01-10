import random
import smtplib

from settings.constants import TAN_CODE_COUNT_PER_GENERATION as TAN_COUNT


def generate_tan_codes() -> set():
    tan_codes = set()

    for _ in range(TAN_COUNT):
        tan_codes.add(str(random.getrandbits(200)))

    return tan_codes


def send_tan_codes(email) -> tuple:
    """
    Tries to generate tan codes and send them to the user's email
    returns the generated tan_codes and a boolean indicating if it was successfull
    """
    tan_codes = generate_tan_codes()
    email_body = 'Your TAN codes are:\n'.format('\n'.join(tan_codes))
    success = send_email('', '', email, 'TAN Codes', email_body)

    return tan_codes, success


def send_email(sender_username, sender_password, recipient, subject, body):
    gmail_user = sender_username
    gmail_pwd = sender_password
    FROM = sender_username
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
        return True
    except:
        print("failed to send mail")
        return False
