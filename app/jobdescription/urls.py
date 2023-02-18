"""URLs for jobdescription API"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from jobdescription import views

router = DefaultRouter()

# this app name will be utilized in reverse function
app_name = "jobdescription"
router.register("jobdescriptions", views.JobDescriptionViewSet)


urlpatterns = [
    path("", include(router.urls))
]