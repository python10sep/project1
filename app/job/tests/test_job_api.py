"""Test for job API"""

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.models import (JobTitle, JobDescription, Applicant, Portal)
from job.serializers import (
    JobTitleSerializer,
    JobDescriptionSerializer,
    # ApplicantSerializer,
    PortalSerializer
)

JOB_TITLE_URL = reverse("jobtitle:jobtitle-list")


def create_job_title(user, portal, job_description, **params):
    """create and return a sample job_title"""

    defaults = {
        "title": "Simple Job Title"
    }
    defaults.update(params)
    job_title = JobTitle.objects.create(
        user=user,
        job_description=job_description,
        portal=portal,
        **params
    )
    return job_title


class PublicJobTitleApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth required tp call API"""

        res = self.client.get(JOB_TITLE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateJobTitleApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self) -> None:
        """test fixtures"""

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@example.com",
            "password@321"
        )
        self.portal = Portal.objects.create(
            name="naukri1.com",
            description="popular website for job hunting"
        )
        self.job_description = JobDescription.objects.create(
            role="To build backend microservices1",
            description_text="should know git, CICD, linux and must know Python",
            pub_date=timezone.now()
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_job_titles(self):
        """Test retrieving a list of job titles."""

        self.portal.refresh_from_db()
        self.job_description.refresh_from_db()
        self.user.refresh_from_db()

        create_job_title(
            user=self.user,
            title="Python developer",
            portal=self.portal,
            job_description=self.job_description
        )
        create_job_title(
            user=self.user,
            title="Java developer",
            portal=self.portal,
            job_description=self.job_description
        )

        res = self.client.get(JOB_TITLE_URL)

        breakpoint()
        job_titles = JobTitle.objects.all().order_by('-id')
        serializer = JobTitleSerializer(job_titles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_job_title_list_limited_to_user(self):
        """Test list of job titles is limited to authenticated user"""

        self.portal.refresh_from_db()
        self.job_description.refresh_from_db()
        self.user.refresh_from_db()

        other_user = get_user_model().objects.create_user(
            "other@example.com",
            "password@321",
        )

        create_job_title(
            user=self.other_user,
            title="Python developer",
            portal=self.portal,
            job_description=self.job_description
        )
        create_job_title(
            user=self.other_user,
            title="Java developer",
            portal=self.portal,
            job_description=self.job_description
        )

        res = self.client.get(JOB_TITLE_URL)

        job_titles = JobTitle.objects.filter(user=self.user)
        serializer = JobTitleSerializer(job_titles, many=True)
        self.assertEqual(res.data, serializer.data)
