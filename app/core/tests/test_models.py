"""
Test the models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

# `get_user_model()` is a helper function.
#
# This function provides us default user model.
#
# It is best practice to use `get_user_model()` function in order to get
# reference to default user model.
#
# as long as you are using `get_user_model()`, you will get your custom user
# model.
#


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""

        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""

        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "password@321")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email address raises
        ValueError"""

        # TODO: you can also try following commented code.
        # Refer :
        # https://docs.python.org/dev/library/unittest.html#unittest.TestCase.assertRaises

        # with self.assertRaises(ValueError):
        #     get_user_model().objects.create_user("", "password@321")

        self.assertRaises(
            ValueError,
            get_user_model().objects.create_user,
            "",
            "password@321"
        )

    def test_create_super_user(self):
        """Test creating a super user"""

        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "password@321"
        )

        # `is_superuser` comes from `PermissionMixin` class
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
