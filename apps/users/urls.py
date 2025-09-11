from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewset

router = DefaultRouter()

router.register(r'users', UserViewset, basename='user')

urlpatterns = [
    path('', include(router.urls))
]
