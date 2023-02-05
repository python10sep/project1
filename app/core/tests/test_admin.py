"""
Tests for the django admin modifications
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin"""

    def setUp(self) -> None:
        """Create user and client"""

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="adminpass123",
        )

        # why using force login?
        # requires no input from user Y/N
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123",
            name="Test User"
        )

    # admin modifications
    def test_user_list(self):
        """Test that users are listed on page"""

        # TODO (TOPIC - Reversing admin URLs)- refer
        #  https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#reversing-admin-urls
        # also known as `named urls`
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works"""

        # TODO (TOPIC - Reversing admin URLs) - refer
        #  https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#reversing-admin-urls
        # also known as `named urls`
        # matches with admin url to edit user
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_group(self):
        """Test the create user page works"""

        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
