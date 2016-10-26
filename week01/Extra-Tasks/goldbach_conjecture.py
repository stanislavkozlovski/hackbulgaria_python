"""
Implement a function, called goldbach(n) which returns a list of tuples, that is the goldbach conjecture for the given number n.

The Goldbach Conjecture states:

Every even integer greater than 2 can be expressed as the sum of two primes.
Keep in mind that there can be more than one combination of two primes, that sums up to the given number.

The result should be sorted by the first item in the tuple.

For example:

4 = 2 + 2
6 = 3 + 3
8 = 3 + 5
10 = 3 + 7 = 5 + 5
100 = 3 + 97 = 11 + 89 = 17 + 83 = 29 + 71 = 41 + 59 = 47 + 53
Signature

def goldbach(n):
    pass
Test examples
"""


# uses sundaram's sieve to get all the prime numbers below given N
def sundaram3(max_n):
    numbers = list(range(3, max_n+1, 2))
    half = (max_n)//2
    initial = 4

    for step in range(3, max_n+1, 2):
        for i in range(initial, half, step):
            numbers[i-1] = 0
        initial += 2*(step+1)

        if initial > half:
            return [2] + list(filter(None, numbers))


def goldbach(n):
    conjecture = []
    primes = sundaram3(n)

    # iterate through the primes list and then through the primes list where each prime is less than
    # half of N. That way we can get each combination that equals N and won't have any repeating combinations
    for prime_1 in primes:
        for prime_2 in filter(lambda x: x < n//2, primes):
            if prime_1 + prime_2 == n:
                conjecture.append((prime_2, prime_1))

    return conjecture

print(sorted(goldbach(100), key=lambda x: x[0]))
