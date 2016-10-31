"""
We are going to train our OOP skill by implementing a few classes, which will represent a cash desk.

The cash desk will do the following things:

Take money as single bills
Take money as batches (пачки!)
Keep a total count
Tell us some information about the bills it has
The Bill class

Create a class, called Bill which takes one parameter to its constructor - the amount of the bill - an integer.

This class will only have dunders so you wont be afraid of them anymore!

The class should implement:

__str__ and __repr__
__int__
__eq__ and __hash__
If amount is negative number, raise an ValueError error.
If type of amount isn't int, raise an TypeError error.
"""


class Bill:

    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        return "A {}$ bill".format(self.value)

    def __repr__(self):
        return self.__str__()

    def __int__(self):
        try:
            int_val = int(self.value)
        except ValueError as e:
            raise TypeError(e)
        if int_val < 0:
            raise ValueError("The Bill's value cannot be negative!")

        return int_val

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.__str__())


a = Bill(10)
b = Bill(5)
c = Bill(10)

int(a) # 10
str(a) # "A 10$ bill"
print(a) # A 10$ bill

a == b # False
a == c # True

money_holder = {}

money_holder[a] = 1 # We have one 10$ bill

if c in money_holder:
    money_holder[c] += 1

print(money_holder) # { "A 10$ bill": 2 }


"""
The BatchBill class

We are going to implement a class, which represents more than one bill. A BatchBill!

The class takes a list of Bills as the single constructor argument.

The class should have the following methods:

__len__(self) - returns the number of Bills in the batch
total(self) - returns the total amount of all Bills in the batch
We should be able to iterate the BatchBill class with a for-loop.
"""

class BatchBill():

    def __init__(self, bills: list):
        self.bills = bills

    def __len__(self):
        return len(self.bills)

    def __getitem__(self, index):
        return self.bills[index]

    def __int__(self):
        return self.total()

    def total(self):
        """ returns the total amount of dollars we have in the batch"""
        return sum(bill for bill in self.bills)

print('-'*20)
print('BATCH BILL')
print('-'*20)
values = [10, 20, 50, 100]
bills = [Bill(value) for value in values]

batch = BatchBill(bills)

for bill in batch:
    print(bill)

# A 10$ bill
# A 20$ bill
# A 50$ bill
# A 100$ bill

"""
The CashDesk classs

Finally, implement a CashDesk class, which has the following methods:

take_money(money), where money can be either Bill or BatchBill class
total() - returns the total amount of money currenly in the desk
inspect() - prints a table representation of the money - for each bill, how many copies of it we have.
"""

class CashDesk():
    # dict with Key: a Bill object and value the count of bills
    money = {}

    def take_money(self, money):
        if isinstance(money, Bill):
            if money not in self.money.keys():
                self.money[money] = 0
            self.money[money] += 1
        elif isinstance(money, BatchBill):
            for bill in money:
                if bill not in self.money.keys():
                    self.money[bill] = 0
                self.money[bill] += 1

    def total(self):
        return sum(int(bill) for bill in self.money.keys())

    def inspect(self):
        for bill, count in self.money.items():
            print("{}$ bills - {}".format(bill.value, count))

print('-'*20)
print('CASH DESK')
print('-'*20)
values = [10, 20, 50, 100, 100, 100]
bills = [Bill(value) for value in values]

batch = BatchBill(bills)

desk = CashDesk()

desk.take_money(batch)
desk.take_money(Bill(10))

print(desk.total()) # 390
desk.inspect()

# We have a total of 390$ in the desk
# We have the following count of bills, sorted in ascending order:
# 10$ bills - 2
# 20$ bills - 1
# 50$ bills - 1
# 100$ bills - 3