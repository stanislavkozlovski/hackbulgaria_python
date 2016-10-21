"""
Implement the function count_substrings(haystack, needle). It returns the count of occurrences of the string needle in the string haystack.

Don't count overlapped substrings and take case into consideration! For overlapping substrings, check the "baba" example below.
"""
def count_substrings(haystack: str, needle: str):
    return haystack.count(needle)

print("-"*20)
print("COUNT SUBSTRINGS")
print("-"*20)
print(count_substrings("Python is an awesome language to program in!", "o"))
# 4
print(count_substrings("We have nothing in common!", "really?"))
# 0
print(count_substrings("This is this and that is this", "this"))  # "This" != "this"
# 2


"""
You are given a NxM matrix of integer numbers.

Implement a function, called sum_matrix(m) that returns the sum of all numbers in the matrix.

The matrix will be represented as nested lists in Python.
"""
def sum_matrix(m):
    return sum(sum(row) for row in m)

print("-"*20)
print("SUM MATRIX")
print("-"*20)
m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(sum_matrix(m))
# 45
m = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
print(sum_matrix(m))
# 0
m = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
print(sum_matrix(m))
# 55

"""
In most programming languages, NaN stands for Not a Number.

If we take a look at the following JavaScript code:

typeof NaN === 'number' // true
We will see that in JavaScript, NaN stands for Not a NaN, which is recursive by nature.

Implement a Python function, called nan_expand(times), which returns the expansion of NaN (In JavaScript terms :P) that many times.

For example:

If we expand NaN once (times=1), we will have "Not a NaN"
If we expand NaN twice (times=2), we will have "Not a Not a NaN"
If times=3, we have "Not a Not a Not a NaN"
And so on ...

"""
def nan_expand(count: int):
    nan = ""  # type: str
    if count <= 0:
        # return an empty string
        pass
    else:
        nan = "Not a NaN"  # count == 1
        # continue adding if count > 1
        for _ in range(1, count):
            nan = "Not a " + nan

    return nan

print("-"*20)
print("NOT A NAN")
print("-"*20)
print(nan_expand(0))
# ""
print(nan_expand(1))
# "Not a NaN"
print(nan_expand(2))
# "Not a Not a NaN"
print(nan_expand(3))
# "Not a Not a Not a NaN"

"""
Given an integer n, we can factor it in the following form:

n = p1^a1 * p2^a2 * ... * pn^an
Where each p is a prime number and each a is an integer and p^a means p to the power of a.

This is called prime factorization.

Lets see few examples:

10 = 2^1 * 5^1
25 = 5^2
356 = 2^2 * 89 ^ 1
Implement a function, called prime_factorization(n), which takes an integer and returns a list of tuples (pi, ai) that is the result of the factorization.

The list should be sorted in increasing order of the prime numbers.
"""
def get_prime_factors(n):
    """ returns the prime factors of a given number """
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def prime_factorization(n: int):
    prime_factors = get_prime_factors(n)
    from collections import Counter
    return sorted(Counter(prime_factors).most_common(), key=lambda x: x[0])

print("-"*20)
print("PRIME FACTORIZATION")
print("-"*20)
print(prime_factorization(10))
# [(2, 1), (5, 1)] # This is 2^1 * 5^1
print(prime_factorization(14))
# [(2, 1), (7, 1)]
print(prime_factorization(356))
# [(2, 2), (89, 1)]
print(prime_factorization(89))
# [(89, 1)] # 89 is a prime number
print(prime_factorization(1000))
# [(2, 3), (5, 3)]


"""
We are going to implement a very helpful function, called group.

group takes a list of things and returns a list of group, where each group is formed by all equal consecutive elements in the list.

For example:

group([1, 1, 1, 2, 3, 1, 1]) == [[1, 1, 1], [2], [3], [1, 1]]
group([1, 2, 1, 2, 3, 3]) == [[1], [2], [1], [2], [3, 3]]
"""
def group(arr: list):
    master_group = []
    last_num = arr[0]
    curr_group = []  # the group of consecutive numbers
    for num in arr:
        if num != last_num:  # if  the consecutive streak has ended, add the streak to the master group and start counting
            master_group.append(curr_group)  # add the group
            curr_group = []  # reset the current group

        curr_group.append(num)
        last_num = num

    master_group.append(curr_group)  # add the last group
    return master_group

print('-'*20)
print("GROUP")
print('-'*20)
print(group([1, 1, 1, 2, 3, 1, 1]))
# [[1, 1, 1], [2], [3], [1, 1]]
print(group([1, 2, 1, 2, 3, 3]))
# [[1], [2], [1], [2], [3, 3]]


"""
Implement the function max_consecutive(items), which takes a list of things and returns an integer - the count of elements in the longest subsequence of equal consecutive elements.

For example, in the list [1, 2, 3, 3, 3, 3, 4, 3, 3], the result is 4, where the longest subsequence is formed by 3, 3, 3, 3

Test examples
>>> max_consecutive([1, 2, 3, 3, 3, 3, 4, 3, 3])
4
>>> max_consecutive([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5])
3
"""

def max_consecutive(items: list):
    return max([len(gr) for gr in group(items)])

print('-'*20)
print("MAX CONSECUTIVE")
print('-'*20)

print(max_consecutive([1, 2, 3, 3, 3, 3, 4, 3, 3]))
# 4
print(max_consecutive([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5]))
# 3
print(max_consecutive([1, 1, 1, 1, 1]))
# 5