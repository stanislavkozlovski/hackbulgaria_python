from django.test import TestCase
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
        response = self.client.post('/accounts/register/', data={
            'email': 'thebestman@abv.bg', 'first_name': 'What', 'last_name': 'Huh', 'password': 'Lalala123'
        })

        self.assertRedirects(response, '/profile')
        self.assertEqual(User.objects.count(), 1)
        registered_user = User.objects.first()
        self.assertIsInstance(registered_user, User)
        self.assertEqual(registered_user.email, 'thebestman@abv.bg')
        self.assertEqual(registered_user.first_name, 'What')
        self.assertEqual(registered_user.last_name, 'Huh')
        # Should be encrypted
        self.assertNotEqual(registered_user.password, 'Lalala123')

    def test_invalid_email_should_not_register(self):
        response = self.client.post('/accounts/register', data={
            'email':'123', first_name:'What', last_name:'Huh', password:'Lala'
        })

        self.assertRedirects(response, '/')
        self.assertEqual(User.objects.count(), 0)

    def test_invalid_password_should_not_register(self):
        response = self.client.post('/accounts/register', data={
            'email': 'mem@abv.bg', first_name: 'What', last_name: 'Huh', password: 'La'
        })

        self.assertRedirects(response, '/')
        self.assertEqual(User.objects.count(), 0)

    def test_no_firstname_should_not_register(self):
        response = self.client.post('/accounts/register', data={
            'email': '123', first_name: '', last_name: 'Huh', password: 'Lala'
        })

        self.assertRedirects(response, '/')
        self.assertEqual(User.objects.count(), 0)
