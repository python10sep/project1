"""
Test the models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone


# we have to import `models` from `core`
# instead of importing it from `app.core`
# Because `core` is registered as an application in installed_apps (settings.py)
from core import models


class ModelTests(TestCase):
    """testing of models"""

    def test_create_user_with_email_as_default(self):
        """test creating a user with just email field and password alone"""

        email = "test@example.com"
        password = "test@pass123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_superuser)

    def test_new_user_email_normalization(self):
        """Test that email address enter by user is being stored in DB
        in normalized format"""

        samples_emails = [
            ["test1@EXAMPLE.COM", "test1@example.com"],
            ["Test2@example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.com", "test4@example.com"],
        ]

        for email, expected in samples_emails:
            user = get_user_model().objects.create_user(email, "randompass@321")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """
        Tests that creating using without email address will raise errors.

        Returns:

        """

        # TODO (Topic: usage of assertRaises)
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises
        self.assertRaises(
            ValueError, get_user_model().objects.create_user, "", "password@321"
        )

    def test_new_user_with_short_password(self):
        """Tests that new user cannot be created with short password (< 5)"""

        self.assertRaises(
            ValueError, get_user_model().objects.create_user, "test@example.com", "pass"
        )

    def test_new_user_as_superuser(self):
        """Test that new user created as superuser should have
        is_superuser=True
        """

        user = get_user_model().objects.create_superuser(
            "test@example.com", "password@321"
        )

        # the value of `is_superuser` attr is set to True when used
        # `create_superuser` method
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_job_title(self):
        """Test creating a job title is successful"""

        user = get_user_model().objects.create_user(
            "test@example.com",
            "password@123"
        )

        portal = models.Portal.objects.create(
            name="naukri.com",
            description="popular website for job hunting"
        )
        job_description = models.JobDescription.objects.create(
            role="To build backend microservices",
            description_text="should know git, CICD, linux and must know Python",
            pub_date=timezone.now()
        )
        job_title = models.JobTitle.objects.create(
            user=user,
            title="Python developer",
            job_description=job_description,
            portal=portal
        )

        self.assertEqual(str(portal), portal.name)
        self.assertEqual(
            str(job_title),
            job_title.title + f" ( {job_title.portal} )")
