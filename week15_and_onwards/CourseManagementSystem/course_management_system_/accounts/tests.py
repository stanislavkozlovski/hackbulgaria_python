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

    def test_logged_in_register_post_should_redirect(self):
        # Original registration
        self.client.post('/accounts/register', data={
            'email': 'thebestman@abv.bg', 'first_name': 'What', 'last_name': 'Huh', 'password': 'Lalala123'
        })
        user = User.objects.first()
        self.assertIn('user', self.client.session)
        orig_sess_user = self.client.session['user']

        # Try to register again
        response: HttpResponse = self.client.post('/accounts/register', data={
            'email': 'thebestman22@abv.bg', 'first_name': 'What', 'last_name': 'Huh', 'password': 'Lalala123'
        }, follow=True)
        self.assertRedirects(response, f'/accounts/{user.id}')
        # assert we have not logged in as somebody else
        self.assertEqual(self.client.session['user'], orig_sess_user)

    def test_logged_in_register_GET_should_redirect(self):
        # Original registration
        self.client.post('/accounts/register', data={
            'email': 'thebestman@abv.bg', 'first_name': 'What', 'last_name': 'Huh', 'password': 'Lalala123'
        })
        orig_sess_user = self.client.session['user']
        self.assertIn('user', self.client.session)
        user = User.objects.first()

        response: HttpResponse = self.client.get('/accounts/register', data={
            'email': 'thebestman22@abv.bg', 'first_name': 'What', 'last_name': 'Huh', 'password': 'Lalala123'
        }, follow=True)
        self.assertRedirects(response, f'/accounts/{user.id}')
        self.assertEqual(self.client.session['user'], orig_sess_user)

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
        }, follow=True)
        # Should redirect to the user's profile
        self.assertRedirects(response, '/accounts/1')
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
        # Hacky way to remove a variable from the session
        ss = self.client.session
        del ss['user']
        ss.save()

    def test_login_get_page(self):
        response: HttpResponse = self.client.get('/accounts/login')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logged_in_post_should_redirect_to_profile(self):
        self.client.post('/accounts/register', data={
            'email': 'newman@abv.bg', 'first_name': 'What', 'last_name': 'Huh', 'password': self.user_password
        })
        user = User.objects.last()

        self.assertIn('user', self.client.session)  # We are logged in
        orig_sess_user = self.client.session['user']
        response: HttpResponse = self.client.post('/accounts/login', data={'email': 'mee@abv.bg', 'password': '1234567'},
                                                  follow=True)
        self.assertRedirects(response, f'/accounts/{user.id}')
        # assert we have not logged in as somebody else
        self.assertEqual(self.client.session['user'], orig_sess_user)

    def test_logged_in_GET_should_redirect_to_profile(self):
        self.client.post('/accounts/register', data={
            'email': 'newman@abv.bg', 'first_name': 'What', 'last_name': 'Huh', 'password': self.user_password
        })
        user = User.objects.last()
        self.assertIn('user', self.client.session)  # We are logged in
        response: HttpResponse = self.client.get('/accounts/login', follow=True)
        self.assertRedirects(response, f'/accounts/{user.id}')

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


class ProfileTests(TestCase):
    def setUp(self):
        # Create a user
        self.client.post('/accounts/register', data={
            'email': 'thebestman@abv.bg', 'first_name': 'What', 'last_name': 'Huh', 'password': 'Lalala123'
        })
        self.user = User.objects.first()

    def test_template_used(self):
        response: HttpResponse = self.client.get(f'/accounts/{self.user.id}')
        self.assertTemplateUsed(response, 'profile.html')

    def test_redirects_when_not_logged_in(self):
        # Imitate logging out
        s = self.client.session
        del s['user']
        s.save()

        response: HttpResponse = self.client.get(f'/accounts/{self.user.id}')
        self.assertRedirects(response, '/login')