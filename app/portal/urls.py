"""URLs for portal API"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from portal import views

router = DefaultRouter()

# this app name will be utilized in reverse function
app_name = "portal"
router.register("portals", views.PortalViewSet)


urlpatterns = [
    path("", include(router.urls))
]