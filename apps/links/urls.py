from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import LinkViewset

router = DefaultRouter()

router.register(r'links', LinkViewset, basename='links')

urlpatterns = [
    path('', include(router.urls))
]