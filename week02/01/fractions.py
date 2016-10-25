"""
Implement a function, called simplify_fraction(fraction) that takes a tuple of the form (nominator, denominator) and simplifies the fraction.

The function should return the fraction in it's irreducible form.

For example, a fraction 3/9 can be reduced by dividing both the nominator and the denominator by 3. We end up with 1/3 which is irreducible.

"""



def simplify_fraction(fraction):
    nominator, dividor = fraction
    fraction_gcd = gcd(nominator, dividor)

    return (nominator / fraction_gcd, dividor / fraction_gcd)

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


print(simplify_fraction((3,9)))
# (1,3)
print(simplify_fraction((1,7)))
# (1,7)
print(simplify_fraction((4,10)))
# (2,5)
print(simplify_fraction((63,462)))
# (3,22)


"""
Implement a function, called sort_fractions(fractions) where fractions is a list of tuples of the form (nominator, denominator).

Both the nominator and the denominator are integers.

The function should return the list, sorted in increasing order.
"""


def sort_fractions(fractions):
    return sorted(fractions, key=lambda x: x[0] / x[1])

print(sort_fractions([(2, 3), (1, 2)]))
# [(1, 2), (2, 3)]
print(sort_fractions([(2, 3), (1, 2), (1, 3)]))
# [(1, 3), (1, 2), (2, 3)]
print(sort_fractions([(5, 6), (22, 78), (22, 7), (7, 8), (9, 6), (15, 32)]))
# [(22, 78), (15, 32), (5, 6), (7, 8), (9, 6), (22, 7)]
