from math import factorial

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from mysite.utils.rle_compressor import compress, decompress
from mysite.utils.calculator import get_nth_fibonacci_numbers, get_nth_prime_numbers, gen_primes


def get_index(request):
    return render(request, 'index.html', request.session)


# @/calculateNFactorial
def calc_n_factorial(request: HttpRequest):
    n = request.POST.get('n_fac', '')
    try:
        n = int(n)
        request.session['wanted_n_fac'] = n
        request.session['n_factorial'] = factorial(n)
    except ValueError:
        request.session['error_msg'] = 'The input must be a valid integer!'

    return redirect('index')


# @/calculateNthFibonacci
def calc_nth_fibonacci_numbers(request: HttpRequest):
    """ Calculate the fibonacci numbers up to n"""
    n = request.POST.get('n_fib', '')
    try:
        n = int(n)

        if n <= 0:
            request.session['error_msg'] = 'The input must be a positive integer!'
            return redirect('index')

        request.session['wanted_n_fibonaccis'] = n
        request.session['fibonaccis'] = get_nth_fibonacci_numbers(n)
    except ValueError:
        request.session['error_msg'] = 'The input must be a valid integer!'

    return redirect('index')


# @/calculateNthPrimes
def calc_nth_primes(request: HttpResponse):
    """ Calculate the first N prime numbers """
    n = request.POST.get('n_primes', '')
    try:
        n = int(n)

        if n > 1000 or n < 1:
            request.session['error_msg'] = 'The input must be between 1 and 1000!'
            return redirect('index')

        request.session['wanted_n_primes'] = n
        request.session['primes'] = get_nth_prime_numbers(n)
    except ValueError:
        request.session['error_msg'] = 'The input must be a valid integer!'

    return redirect('index')


# @/encodeRL
def encode_rl(request: HttpResponse):
    string = request.POST.get('str_to_encode', '')

    try:
        encoded_str = compress(string)
    except ValueError as e:
        request.session['error_msg'] = str(e)
        return redirect('index')
    request.session['wanted_enc_str'] = string
    request.session['encoded_str'] = encoded_str

    return redirect('index')


# @/decodeRL
def decode_rl(request: HttpResponse):
    encoded_string = request.POST.get('str_to_decode', '')

    try:
        decoded_str = decompress(encoded_string)
    except ValueError as e:
        request.session['error_msg'] = str(e)
        return redirect('index')

    request.session['wanted_dec_str'] = encoded_string
    request.session['decoded_str'] = decoded_str

    return redirect('index')

