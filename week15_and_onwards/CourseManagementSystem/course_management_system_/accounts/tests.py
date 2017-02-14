from django.test import TestCase
from django.http import HttpResponse

from accounts.models import User


# Create your tests here.
class UserModelTests(TestCase):
    def test_their_emails_are_unique(self):
        user = User.objects.create(email='someguy@abv.bg', password='123')
        with self.assertRaises(Exception):
            User.objects.create(email='someguy@abv.bg', password='123')


class RegisterTests(TestCase):
    def test_register_view(self):
        response = self.client.get('/accounts/register')

        self.assertTemplateUsed(response, 'register.html')
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        response = self.client.post('/accounts/register', data={
            'email': 'thebestman@abv.bg', 'first_name': 'What', 'last_name': 'Huh', 'password': 'Lalala123'
        })

        self.assertEqual(User.objects.count(), 1)
        registered_user = User.objects.first()
        self.assertRedirects(response, f'/accounts/{registered_user.id}')
        self.assertIsInstance(registered_user, User)
        self.assertEqual(registered_user.email, 'thebestman@abv.bg')
        self.assertEqual(registered_user.first_name, 'What')
        self.assertEqual(registered_user.last_name, 'Huh')
        # Should be encrypted
        self.assertNotEqual(registered_user.password, 'Lalala123')

    def test_invalid_email_should_not_register(self):
        response = self.client.post('/accounts/register', data={
            'email':'123', 'first_name':'What', 'last_name':'Huh', 'password':'Lala'
        })

        self.assertRedirects(response, '/accounts/register')
        self.assertEqual(User.objects.count(), 0)

    def test_duplicate_email_should_not_register(self):
        # Create the first user
        response = self.client.post('/accounts/register', data={
            'email': 'thebestman@abv.bg', 'first_name': 'What', 'last_name': 'Huh', 'password': 'Lalala123'
        })

        self.assertEqual(User.objects.count(), 1)

        # Try to create a second identical one
        response = self.client.post('/accounts/register', data={
            'email': 'thebestman@abv.bg', 'first_name': 'What', 'last_name': 'Huh', 'password': 'Lalala123'
        })
        self.assertRedirects(response, '/accounts/register')
        self.assertEqual(User.objects.count(), 1)  # Should not have added another user

    def test_invalid_password_should_not_register(self):
        response = self.client.post('/accounts/register', data={
            'email': 'mem@abv.bg', 'first_name': 'What', 'last_name': 'Huh', 'password': 'La'
        })

        self.assertRedirects(response, '/accounts/register')
        self.assertEqual(User.objects.count(), 0)

    def test_no_firstname_should_not_register(self):
        response = self.client.post('/accounts/register', data={
            'email': '123', 'first_name': '', 'last_name': 'Huh', 'password': 'Lala'
        })

        self.assertRedirects(response, '/accounts/register')
        self.assertEqual(User.objects.count(), 0)


class LoginTests(TestCase):
    def setUp(self):
        # register a user
        self.user_email = 'thebestman@abv.bg'
        self.user_password = 'Lalala123'

        self.client.post('/accounts/register', data={
            'email': self.user_email, 'first_name': 'What', 'last_name': 'Huh', 'password': self.user_password
        })
        self.user = User.objects.first()

    def test_login_get_page(self):
        response: HttpResponse = self.client.get('/accounts/login')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_invalid_email_should_not_login(self):
        response: HttpResponse = self.client.post('/accounts/login', data={'email': 'mee@abv.bg', 'password': '1234567'})

        self.assertRedirects(response, '/accounts/login')
        self.assertNotIn('user', self.client.session)

    def test_invalid_password_should_not_login(self):
        response: HttpResponse = self.client.post('/accounts/login', data={'email': self.user_email, 'password': '1234567'})

        self.assertRedirects(response, '/accounts/login')
        self.assertNotIn('user', self.client.session)

    def test_valid_login(self):
        response: HttpResponse = self.client.post('/accounts/login',
                                                  data={'email': self.user_email, 'password': self.user_password})

        self.assertRedirects(response, f'/accounts/{self.user.id}')
        self.assertIn('user', self.client.session)
