from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AccountViewsTests(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("site_nav", response.context)

    def test_register_view_post_valid(self):
        data = {
            "email": "test@testing.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
            "full_name": "Jane Doe",
            "bio": "Tester",
        }
        response = self.client.post(reverse("register"), data=data)
        assert response.status_code == 302
        assert User.objects.filter(email="test@testing.com").exists()

    def test_login_view(self):
        _ = User.objects.create_user(email="bob@testing.com", password="pass123")
        response = self.client.post(
            reverse("login"),
            data={"username": "bob@testing.com", "password": "pass123"},
        )
        assert response.status_code == 302
        # self.assertRedirects(response, reverse("profile"))

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse("profile"))
        assert response.status_code == 302
        # self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_profile_view_logged_in(self):
        _ = User.objects.create_user(email="alice@testing.com", password="pass123")
        self.client.login(username="alice@testing.com", password="pass123")
        response = self.client.get(reverse("profile"))
        assert response.status_code == 200
        assert "site_nav" in response.context

    def test_edit_profile_view_post(self):
        _ = User.objects.create_user(email="eve@testing.com", password="pass123")
        self.client.login(username="eve@testing.com", password="pass123")
        response = self.client.post(
            reverse("edit_profile"), {"full_name": "Eve Adams", "bio": "Bio"}
        )
        assert response.status_code == 200
        # self.assertRedirects(response, reverse("profile"))
