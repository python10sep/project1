from django.urls import path, include
from rest_framework.routers import DefaultRouter

from job import views

# `DefaultRouter` provided by DRF automatically creates URL routing for us.
router = DefaultRouter()
router.register("jobtitles", views.JobTitleViewSet)

# this name is used by reverse function
app_name = "jobtitle"

urlpatterns = [
    path("", include(router.urls))
]