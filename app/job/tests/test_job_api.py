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
    JobTitleDetailSerializer,
    JobDescriptionSerializer,
    # ApplicantSerializer,
    PortalSerializer
)

JOB_TITLE_URL = reverse("jobtitle:jobtitle-list")


def detail_url(job_title_id):
    """create and return a job title detail URL"""

    return reverse("jobtitle:jobtitle-detail", args=[job_title_id])


def create_job_description(**params):
    """create and return new job description"""

    defaults = {
        "title": "Simple Job Title",
        "description_text": "should know git, CICD, linux and must know Python",
        "pub_date": timezone.now()
    }
    defaults.update(params)
    job_description = JobDescription.objects.create(
        role="To build backend microservices1",
        description_text="should know git, CICD, linux and must know Python",
        pub_date=timezone.now()
    )
    return job_description


def create_job_title(user, portal, job_description, **params):
    """create and return a sample job_title"""

    defaults = {
        "title": "Simple Job Title",
    }

    # we need new `JobDescription` for every `JobTitle`

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

        create_job_title(
            user=self.user,
            title="Python developer",
            portal=self.portal,
            job_description=create_job_description()
        )
        create_job_title(
            user=self.user,
            title="Java developer",
            portal=self.portal,
            job_description=create_job_description()
        )

        # If you need to reload a model’s values from the database,
        # you can use the refresh_from_db() method.
        # TODO - refer
        #  https://docs.djangoproject.com/en/4.1/ref/models/instances/#refreshing-objects-from-database
        # NOTE - should be used when doing `delete` operations specifically.
        self.portal.refresh_from_db()
        self.job_description.refresh_from_db()
        self.user.refresh_from_db()

        res = self.client.get(JOB_TITLE_URL)

        job_titles = JobTitle.objects.all().order_by('-id')
        serializer = JobTitleSerializer(job_titles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_job_title_list_limited_to_user(self):
        """Test list of job titles is limited to authenticated user"""

        other_user = get_user_model().objects.create_user(
            "other@example.com",
            "password@321",
        )

        create_job_title(
            user=other_user,
            title="Python developer",
            portal=self.portal,
            job_description=create_job_description()
        )
        create_job_title(
            user=other_user,
            title="Java developer",
            portal=self.portal,
            job_description=create_job_description()
        )

        res = self.client.get(JOB_TITLE_URL)

        job_titles = JobTitle.objects.filter(user=self.user)
        serializer = JobTitleSerializer(job_titles, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_get_jobtitle_detail(self):
        """Test get jobtitle detail"""

        other_user = get_user_model().objects.create_user(
            "other@example.com",
            "password@321",
        )

        job_title = create_job_title(
            user=other_user,
            title="Python developer",
            portal=self.portal,
            job_description=create_job_description()
        )
        url = detail_url(job_title.id)
        res = self.client.get(url)

        serializer = JobTitleDetailSerializer(job_title)
        self.assertEqual(res.data, serializer.data)
