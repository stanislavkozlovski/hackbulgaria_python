from django.test import TestCase
from accounts.models import User


# Create your tests here.
class UserModelTests(TestCase):
    def test_their_emails_are_unique(self):
        user = User.objects.create(email='someguy@abv.bg', password='123')
        with self.assertRaises(Exception):
            User.objects.create(email='someguy@abv.bg', password='123')


