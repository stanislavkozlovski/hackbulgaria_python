"""
A Bank Account

BankAccount class, which behaves like that:

Basic BankAccount usage

Our BankAccount will have the following methods:

Constructor takes a name for the account, initial balance and a currency. If balance is negative number, raise an ValueError error.
deposit(amount) - deposits money of amount amount. If amount is negative number, raise an ValueError error.
balance() - returns the current balance
withdraw(amount) - takes amount money from the account. Returns True if it was successful. Otherwise, False
__str__ should print: "Bank account for {name} with balance of {amount}{currency}"
__int__ should return the balance of the BankAccount
transfer_to(account, amount) - transfers amount to account if they both have the same currencies! Returns True if successful.
history() - returns a list of strings, that represent the history of the bank account. Check examples below for more information.
"""


class BankAccount():

    def __init__(self, name: str, balance: float,currency: str):
        self.name = name
        if balance >= 0:
            self._balance = balance
        else:
            raise ValueError('Balance cannot be negative')
        self.currency = currency
        self._history = ['Account was created']  # list with history regarding the account

    def __str__(self):
        return "Bank account for {name} with balance of {amount}{currency}".format(
            name=self.name,
            amount=self._balance,
            currency=self.currency
        )

    def __int__(self):
        self.add_to_history('__int__ check -> {amount}{currency}'.format(amount=self._balance, currency=self.currency))

        return self._balance

    def add_to_history(self, message: str):
        self._history.append(message)

    def history(self):
        return self._history

    def balance(self):
        self.add_to_history('Balance check -> {balance}{currency}'.format(balance=self._balance, currency=self.currency))
        return self._balance

    def deposit(self, amount, from_account: str=''):
        if amount < 0:
            raise ValueError('Amount cannot be negative')
        self._balance += amount

        if from_account:
            # deposit from another account
            self.add_to_history('Transfer from {guy} for {amount}{currency}'.format(
                guy=from_account,
                amount=amount,
                currency=self.currency
            ))
        else:
            self.add_to_history('Deposited {amount}{currency}'.format(amount=amount, currency=self.currency))

    def withdraw(self, amount, transfer=False):
        if amount > self._balance:
            self.add_to_history('Withdraw for {amount}{currency} failed.'.format(amount=amount,currency=self.currency))
            return False

        self._balance -= amount
        if not transfer:
            self.add_to_history('{amount}{currency} was withdrawn'.format(amount=amount, currency=self.currency))
        return True

    def transfer_to(self, account, amount: int):
        if self.currency != account.currency or self._balance < amount:
            return False

        self.withdraw(amount, transfer=True)
        account.deposit(amount, self.name)

        self.add_to_history('Transfer to {guy} for {amount}{currency}'.format(
            guy=account.name,
            amount=amount,
            currency=self.currency
        ))

        return True


account = BankAccount("Rado", 0, "$")
print(account)
#'Bank account for Rado with balance of 0$'
account.deposit(1000)
print(account.balance())
#1000
print(str(account))
#'Bank account for Rado with balance of 1000$'
print(int(account))
#1000
print(account.history())
#['Account was created', 'Deposited 1000$', 'Balance check -> 1000$', '__int__ check -> 1000$']
print(account.withdraw(500))
#True
print(account.balance())
#500
print(account.history())
#['Account was created', 'Deposited 1000$', 'Balance check -> 1000$', '__int__ check -> 1000$', '500$ was withdrawed', 'Balance check -> 500$']
print(account.withdraw(1000))
#False
print(account.balance())
#500
print(account.history())
#['Account was created', 'Deposited 1000$', 'Balance check -> 1000$', '__int__ check -> 1000$', '500$ was withdrawed', 'Balance check -> 500$', 'Withdraw for 1000$ failed.', 'Balance check -> 500$']


rado = BankAccount("Rado", 1000, "BGN")
ivo = BankAccount("Ivo", 0, "BGN")
print(rado.transfer_to(ivo, 500))
# True
print(rado.balance())
# 500
print(ivo.balance())
# 500
print(rado.history())
# ['Account was created', 'Transfer to Ivo for 500BGN', 'Balance check -> 500BGN']
print(ivo.history())
# ['Account was created', 'Transfer from Rado for 500BGN', 'Balance check -> 500BGN']