import getpass
from validate_email import validate_email
from settings.validator import is_valid_password, validate_user
import sql_manager
from utils.password_reset import (generate_password_reset_token, send_password_reset_token,
                                  save_password_reset_token, fetch_user_password_reset_token)


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

            sql_manager.register(username, password, email)

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
            user_exists, user = validate_user(username)
            if not user_exists:
                print('No user with the username {} exists!'.format(username))
            reset_token = generate_password_reset_token()
            email_was_sent = send_password_reset_token(user, reset_token)
            if not email_was_sent:
                print('There was an error with sending the e-mail!')
                return
            save_password_reset_token(user, reset_token)
        elif command.startswith('reset-password'):
            username = command[15:]
            user_exists, user = validate_user(username)
            if not user_exists:
                print('No user with the username {} exists!'.format(username))
                return

            reset_token = fetch_user_password_reset_token(username)
            if reset_token is None:
                print('There is no reset token for the user!')
                return

            given_reset_token = input('Please enter your reset token: ')
            if given_reset_token != reset_token:
                print('Invalid reset token!')
                return

            new_password = getpass.getpass('Enter your new password: ')
            while not is_valid_password(username, new_password):
                new_password = getpass.getpass('Enter your new password: ')

            sql_manager.reset_user_password_reset_token(user)
            sql_manager.change_pass(logged_user=user, new_pass=new_password)
            print('You have successfully reset your password!')
        elif command == 'help':
            print("login - for logging in!")
            print("register - for creating new account!")
            print("exit - for closing program!")
        elif command == 'exit':
            return
        else:
            print("Not a valid command")


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
