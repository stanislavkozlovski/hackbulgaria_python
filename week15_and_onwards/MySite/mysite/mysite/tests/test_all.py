from math import factorial

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from mysite.utils.calculator import get_nth_fibonacci_numbers


class NFactorialTests(TestCase):
    def test_give_n_should_get_factorial(self):
        n = 10
        expected_fact = factorial(n)
        url = reverse('calc_n_factorial')
        response: HttpResponse = self.client.post(url, data={'n_fac': n}, follow=True)

        self.assertContains(response, expected_fact)

    def test_give_invalid_n_should_have_error_msg(self):
        n = 'AaA'
        expected_msg = 'The input must be a valid integer!'
        url = reverse('calc_n_factorial')
        response: HttpResponse = self.client.post(url, data={'n_fac': n}, follow=True)

        self.assertContains(response, expected_msg)

    def test_give_empty_n_should_have_error_msg(self):
        n = ''
        expected_msg = 'The input must be a valid integer!'
        url = reverse('calc_n_factorial')
        response: HttpResponse = self.client.post(url, data={'n_fac': n}, follow=True)

        self.assertContains(response, expected_msg)


class FirstNFibonacciTests(TestCase):
    def test_give_n_should_return_fibonacci_numbers(self):
        n = 5
        expected_numbers = '1, 1, 2, 3, 5'
        url = reverse('calc_first_n_fibonacci')
        response: HttpResponse = self.client.post(url, data={'n_fib': n}, follow=True)

        self.assertContains(response, expected_numbers)

    def test_give_invalid_n_should_display_error_message(self):
        n = ''
        expected_msg = 'The input must be a valid integer!'
        url = reverse('calc_first_n_fibonacci')
        response: HttpResponse = self.client.post(url, data={'n_fib': n}, follow=True)

        self.assertContains(response, expected_msg)

    def test_give_negative_n_should_display_error_message(self):
        n = -5
        expected_msg = 'The input must be a positive integer!'
        url = reverse('calc_first_n_fibonacci')
        response: HttpResponse = self.client.post(url, data={'n_fib': n}, follow=True)

        self.assertContains(response, expected_msg)

    def test_get_nth_fibonacci_numbers(self):
        n = 5
        expected_result = '1, 1, 2, 3, 5'
        result = get_nth_fibonacci_numbers(n)

        self.assertEqual(result, expected_result)


class FirstNPrimesTests(TestCase):
    def test_give_n_should_return_primes(self):
        n = 2
        expected_numbers = '2, 3'
        url = reverse('calc_first_n_primes')
        response: HttpResponse = self.client.post(url, data={'n_primes': n}, follow=True)

        self.assertContains(response, expected_numbers)

    def test_give_big_n_should_show_error(self):
        n = 1001
        expected_msg = 'The input must be between 1 and 1000!'
        url = reverse('calc_first_n_primes')
        response: HttpResponse = self.client.post(url, data={'n_primes': n}, follow=True)

        self.assertContains(response, expected_msg)

    def test_give_negative_n_should_show_error(self):
        n = -5
        expected_msg = 'The input must be between 1 and 1000!'
        url = reverse('calc_first_n_primes')
        response: HttpResponse = self.client.post(url, data={'n_primes': n}, follow=True)

        self.assertContains(response, expected_msg)

    def test_give_invalid_n_should_show_error(self):
        n = 'AaA'

        expected_msg = 'The input must be a valid integer!'
        url = reverse('calc_first_n_primes')
        response: HttpResponse = self.client.post(url, data={'n_primes': n}, follow=True)

        self.assertContains(response, expected_msg)