from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("register"),
            data={
                "username": "muzaffar",
                "first_name": "muzaffar",
                "last_name": "joraboyev",
                "email": "muzaffarmurodogli@gmail.com",
                "password": "anypassword"
            }
        )

        user = User.objects.get(username="muzaffar")

        self.assertEqual(user.first_name, "muzaffar")
        self.assertEqual(user.last_name, "joraboyev")
        self.assertEqual(user.email, "muzaffarmurodogli@gmail.com")
        self.assertNotEqual(user.password, "anypassword")
        self.assertTrue(user.check_password("anypassword"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("register"),
            data={
                "first_name": "muzaffar",
                "email": "muzaffarmurodogli@gmail.com"
            }
        )

        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("register"),
            data={
                "username": "muzaffar",
                "first_name": "muzaffar",
                "last_name": "joraboyev",
                "email": "invalid-email",
                "password": "anypassword"
            }
        )

        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        user = User.objects.create(username="muzaffar", first_name="muzaffar")
        user.set_password("somepass")
        user.save()

        response = self.client.post(
            reverse("register"),
            data={
                "username": "muzaffar",
                "first_name": "muzaffar",
                "last_name": "joraboyev",
                "email": "muzaffarmurodogli@gmail.com",
                "password": "anypassword"
            }
        )

        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")


class LoginTestCase(TestCase):
    def test_successful_login(self):
        db_user = User.objects.create_user(username="muzaffar", firstname="muzaffar")
        db_user.set_password("somepassword")
        db_user.save()

        self.client.post(
            reverse("login"),
            data={
                "username": "muzaffar",
                "password": "anypassword"
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        db_user = User.objects.create_user(username="muzaffar", firstname="muzaffar")
        db_user.set_password("somepassword")
        db_user.save()

        self.client.post(
            reverse("login"),
            data={
                "username": "wrong-username",
                "password": "anypassword"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("login"),
            data={
                "username": "muzaffar",
                "password": "wrong-password"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)