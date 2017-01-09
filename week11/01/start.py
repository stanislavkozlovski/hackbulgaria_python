from settings.validator import is_valid_password
import sql_manager


def main_menu():
    print("Welcome to our bank service. You are not logged in. \nPlease register or login")

    while True:
        command = input("$$$>")

        if command == 'register':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            while not is_valid_password(username, password):
                print('Your password is invalid!')
                password = input("Enter your password: ")

            sql_manager.register(username, password)

            print("Registration Successful")
        elif command == 'login':
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            logged_user = sql_manager.login(username, password)

            if logged_user:
                logged_menu(logged_user)
            else:
                print("Login failed")
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
