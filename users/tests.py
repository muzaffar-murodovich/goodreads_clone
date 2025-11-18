from urllib import response
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('register'),
            data={
                'username': 'muzaffar',
                'first_name': 'muzaffar',
                'last_name': 'joraboyev',
                'email': 'invalid',
                'password': 'anypassword',
            }
        )

        user = User.objects.get(username='')

        self.assertEqual(user.username, '')
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(user.email, '')
        self.assertNotEqual(user.password, '')
        self.assertTrue(user.check_password('somepassword'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('register'),
            data={
                'first_name':'muzaffar',
                "email":"muzaffarmurodogli@gmail.com",
            }
        )
        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse('register'),
            data={
                'username':'muzaffar',
                'first_name':'muzaffar',
                'last_name':'joraboyev',
                'email':'invalid',
                'password':'anypassword',
            }
        )

        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        response = self.client.post(
            reverse('register'),
            data={
                'username':'muzaffar',
                'first_name':'muzaffar',
                'last_name':'joraboyev',
                'email':'muzaffarmurodogli@gmail.com',
                'password':'anypassword',
            }
        )

        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'This username has already been taken.')