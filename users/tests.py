from django.contrib.auth import get_user
from users.models import CustomUser
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

        user = CustomUser.objects.get(username="muzaffar")

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

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)

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

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn("email", form.errors)
        self.assertIn("Enter a valid email address.", str(form.errors['email']))

    def test_unique_username(self):
        user = CustomUser.objects.create(username="muzaffar", first_name="muzaffar")
        user.set_password("anypassword")
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

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn("username", form.errors)
        self.assertIn("A user with that username already exists.", str(form.errors['username']))

class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create_user(username="muzaffar", first_name="muzaffar")
        self.db_user.set_password("anypassword")
        self.db_user.save()

    def test_successful_login(self):

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

    def test_logout(self):

        self.client.login(username="muzaffar", password="anypassword")

        self.client.get(reverse("logout"))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login") + "?next=" + reverse("profile"))

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="muzaffar",
            first_name="muzaffar",
            last_name="joraboyev",
            email="muzaffar@mail.com",
        )
        user.set_password("anypassword")
        user.save()

        self.client.login(username="muzaffar", password="anypassword")

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="muzaffar", first_name="muzaffar", last_name="joraboyev", email="muzaffarmurodogli@gmail.com"
        )
        user.set_password("anypassword")
        user.save()
        self.client.login(username="muzaffar", password="anypassword")

        response = self.client.post(
            reverse("profile_edit"),
            data={
                "username": "muzaffar",
                "first_name": "muzaffar",
                "last_name": "kaktus",
                "email": "muzaffarmurodogli@gmail.com"
            }
        )

        user.refresh_from_db()

        self.assertEqual(user.last_name, "kaktus")
        self.assertEqual(user.email, "muzaffarmurodogli@gmail.com")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("profile"))