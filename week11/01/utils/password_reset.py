""" Functions used to reset the password of a user"""
import smtplib
import uuid

from settings.constants import DB_ID_KEY, DB_USER_EMAIL_KEY


def generate_password_reset_token():
    return uuid.uuid4().hex


def send_password_reset_token(user, token):
    email = user.email
    email_is_sent = send_password_reset_email('placeholder', 'placeholder', recipient=email, subject='Reset your password',
                                                body='You have requested a password reset. Please use this token {}'.format(token))
    return email_is_sent


def send_password_reset_email(sender_username, sender_password, recipient, subject, body):
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


def save_password_reset_token(user, token):
    user.reset_code = token


def fetch_user_password_reset_token(username):
    return fetch_user_reset_token(username)