"""
An Immutable Fraction class

We want to create a simple fraction class:


Our fractions should be able to do the following operations:

+
-
*
==
Implement the needed dunder methods in order to achieve that.

Each operation that mutates the fraction, like +, - and * should return a new Fraction!

Examples:

a = Fraction(1, 2)
b = Fraction(2, 4)

a == b # True

a + b # 1
a - b # 0
a * b # 1 / 4
"""
import math


class Fraction:

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
        self.value = numerator/denominator

    def __str__(self):
        if self.numerator / self.denominator == float(self.numerator // self.denominator):
            return str(math.floor(self.numerator // self.denominator))

        return "{} / {}".format(math.floor(self.numerator), math.floor(self.denominator))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.value == other.value

    def __add__(self, other):
        if self.denominator != other.denominator:
            if self.denominator > other.denominator:
                # get the other fraction to our denominator
                difference = self.denominator / other.denominator
                other = Fraction(numerator=other.numerator * difference,
                                 denominator=other.denominator * difference)
            else:
                # get our denominator the same as the other fraction's
                difference = other.denominator / self.denominator
                self.numerator *= difference
                self.denominator *= difference

        return simplify_fraction(Fraction(numerator=self.numerator + other.numerator,
                                          denominator=self.denominator))

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if self.denominator != other.denominator:
            if self.denominator > other.denominator:
                # get the other fraction to our denominator
                difference = self.denominator / other.denominator
                other = Fraction(numerator=other.numerator * difference,
                                 denominator=other.denominator * difference)
            else:
                # get our denominator the same as the other fraction's
                difference = other.denominator / self.denominator
                self.numerator *= difference
                self.denominator *= difference

        return simplify_fraction(Fraction(numerator=self.numerator - other.numerator,
                                          denominator=self.denominator))

    def __rsub__(self, other):
        if self.denominator != other.denominator:
            if self.denominator > other.denominator:
                # get the other fraction to our denominator
                difference = self.denominator / other.denominator
                other = Fraction(numerator=other.numerator * difference,
                                 denominator=other.denominator * difference)
            else:
                # get our denominator the same as the other fraction's
                difference = other.denominator / self.denominator
                self.numerator *= difference
                self.denominator *= difference

        return simplify_fraction(Fraction(numerator=other.numerator - self.numerator,
                                          denominator=self.denominator))

    def __mul__(self, other):
        return simplify_fraction(Fraction(numerator=self.numerator * other.numerator,
                                          denominator=self.denominator * other.denominator))


def simplify_fraction(fraction: Fraction):
    fraction_gcd = gcd(fraction.numerator, fraction.denominator)

    return Fraction(numerator=fraction.numerator / fraction_gcd,
                    denominator=fraction.denominator / fraction_gcd)


def gcd(a, b) -> int:
    """
    Returns the greatest common divisor for both the numbers using the Euclidean algorithm
    """

    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a

    return b if a == 0 else a


a = Fraction(1, 2)
b = Fraction(2, 4)

print(a == b) # True

print(a + b) # 1
print(a - b) # 0
print(a * b) # 1 / 4