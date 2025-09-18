from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import LinkViewset, ClickViewset

router = DefaultRouter()

router.register(r'links', LinkViewset, basename='links')
router.register(r'clicks', ClickViewset, basename='clicks')

urlpatterns = [
    path('', include(router.urls))
]