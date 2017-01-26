import getpass
from validate_email import validate_email
from settings.validator import is_valid_password, validate_user
import controller
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

            password = input("Enter your password: ")
            while not is_valid_password(username, password):
                print('Your password is invalid!')
                password = input("Enter your password: ")

            controller.register(username, password, email)

            print("Registration Successful")
        elif command == 'login':
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            logged_user = controller.login(username, password)

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
            user.reset_code = reset_token
        elif command.startswith('reset-password'):
            username = command[15:]
            user_exists, user = validate_user(username)
            if not user_exists:
                print('No user with the username {} exists!'.format(username))
                return

            reset_token = user.reset_code
            if not reset_token:
                print('There is no reset token for the user!')
                return

            given_reset_token = input('Please enter your reset token: ')
            if given_reset_token != reset_token:
                print('Invalid reset token!')
                return

            new_password = input('Enter your new password: ')
            while not is_valid_password(username, new_password):
                new_password = input('Enter your new password: ')

            user.reset_code = ''
            user.password = new_password
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
            print("Your id is: " + str(logged_user.id_))
            print("Your balance is:" + str(logged_user.balance) + '$')

        elif command == 'changepass':
            new_pass = input("Enter your new password: ")
            while not is_valid_password(logged_user.username, new_pass):
                print('Your password is invalid!')
                new_pass = input("Enter your new password: ")
            controller.change_password(logged_user, new_pass)
            logged_user.password = new_pass

        elif command == 'change-message':
            new_message = input("Enter your new message: ")
            logged_user.message = new_message

        elif command == 'show-message':
            print(logged_user.message)

        elif command.startswith('deposit'):
            amount = command.split()[-1]
            try:
                amount = float(amount)
                tan_code = input(">Enter TAN code: ")
                if not controller.is_valid_tan_code(logged_user, tan_code):
                    print('Invalid TAN code!')
                    return
                controller.deposit_money(logged_user, amount)
                controller.consume_tan_code(tan_code)

                print('{:.2f} was successfully added to your account!'.format(amount))
            except ValueError:
                print('Invalid deposit amount!')

        elif command.startswith('withdraw'):
            amount = command.split()[-1]
            try:
                amount = float(amount)
                tan_code = input(">Enter TAN code: ")
                if not controller.is_valid_tan_code(logged_user, tan_code):
                    print('Invalid TAN code!')
                else:
                    did_withdraw = controller.withdraw_money(logged_user, amount)
                    if did_withdraw:
                        controller.consume_tan_code(tan_code)
                        print('{:.2f} was successfully withdrawn to your account!'.format(amount))
            except ValueError:
                print('Invalid withdraw amount!')

        elif command == 'generate-tan-codes':
            password = input("Enter your password: ")
            logged_user = controller.login(logged_user.username, password)
            if logged_user:
                controller.generate_tan_codes(logged_user)
            else:
                print("Login failed")

        elif command == 'display-balance':
            print(logged_user.balance)

        elif command == 'help':
            print("info - for showing account info")
            print('deposit <amount> - for depositing money')
            print('withdraw <amount> - for withdrawing money')
            print("changepass - for changing passowrd")
            print("change-message - for changing users message")
            print("show-message - for showing users message")
            print("display-balance - for displaying your current balance")
            print("generate-tan-codes - generates and sends 10 TAN codes to your e-mail")


def main():
    # sql_manager.create_tables()
    main_menu()

if __name__ == '__main__':
    main()
