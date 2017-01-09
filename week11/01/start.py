import getpass
from validate_email import validate_email
from settings.validator import is_valid_password
import sql_manager
import smtplib


def main_menu():
    print("Welcome to our bank service. You are not logged in. \nPlease register or login")

    while True:
        command = input("$$$>")

        if command == 'register':
            username = input("Enter your username: ")
            email = input('Enter your e-mail: ')
            while not validate_email(email):
                print('Your e-mail is invalid!')
                email = input('Enter your e-mail: ')

            password = getpass.getpass("Enter your password: ")
            while not is_valid_password(username, password):
                print('Your password is invalid!')
                password = getpass.getpass("Enter your password: ")

            sql_manager.register(username, password)

            print("Registration Successful")
        elif command == 'login':
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")

            logged_user = sql_manager.login(username, password)

            if logged_user:
                logged_menu(logged_user)
            else:
                print("Login failed")
        elif command.startswith('send-reset-password'):
            username = command[20:]
            # TODO:
            validate_user()
            generate_token()
            send_token()
            save_token()
            pass
        elif command == 'help':
            print("login - for logging in!")
            print("register - for creating new account!")
            print("exit - for closing program!")
        elif command == 'exit':
            return
        else:
            print("Not a valid command")

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
        print('successfully sent the mail'
    except:
        print("failed to send mail")


def logged_menu(logged_user):
    print("Welcome you are logged in as: " + logged_user.username)
    while True:
        command = input("Logged>>")

        if command == 'info':
            print("You are: " + logged_user.username)
            print("Your id is: " + str(logged_user.id))
            print("Your balance is:" + str(logged_user.balance) + '$')

        elif command == 'changepass':
            new_pass = input("Enter your new password: ")
            while not is_valid_password(logged_user.username, new_pass):
                print('Your password is invalid!')
                new_pass = input("Enter your new password: ")
            sql_manager.change_pass(new_pass, logged_user)

        elif command == 'change-message':
            new_message = input("Enter your new message: ")
            sql_manager.change_message(new_message, logged_user)

        elif command == 'show-message':
            print(logged_user.message)

        elif command == 'help':
            print("info - for showing account info")
            print("changepass - for changing passowrd")
            print("change-message - for changing users message")
            print("show-message - for showing users message")


def main():
    sql_manager.create_clients_table()
    main_menu()

if __name__ == '__main__':
    main()
