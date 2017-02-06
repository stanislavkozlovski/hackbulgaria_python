def get_nth_fibonacci_numbers(n) -> str:
    """ Return the first N fibonacci numbers, separated by commas"""
    calculated_fibonaccis = {0: 0, 1: 1}

    def _get_nth_fib(n):
        nonlocal calculated_fibonaccis

        if n in calculated_fibonaccis:
            return calculated_fibonaccis[n]

        calculated_fibonaccis[n] = _get_nth_fib(n-1) + _get_nth_fib(n-2)

        return calculated_fibonaccis[n]

    _get_nth_fib(n)

    return ', '.join(str(calculated_fibonaccis[n]) for n in range(1, n+1))


def get_nth_prime_numbers(n) -> str:
    """ Returns a string containing the first N prime numbers, separated by commas """
    primes = []
    prime_generator = gen_primes()

    for _ in range(n):
        primes.append(str(next(prime_generator)))

    return ', '.join(primes)


def gen_primes():
    calculated_primes = {}

    prime = 2

    while True:
        if prime not in calculated_primes:
            yield prime
            calculated_primes[prime * prime] = [prime]
        else:
            for p in calculated_primes[prime]:
                calculated_primes.setdefault(p + prime, []).append(p)
            del calculated_primes[prime]

        prime += 1
