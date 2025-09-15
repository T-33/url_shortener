from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.links.views import link_redirect_view
urlpatterns = [
    path('<str:short_code>/', link_redirect_view, name='redirect'),
    path('admin/', admin.site.urls),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include('apps.users.urls')),
    path('api/v1/', include('apps.links.urls')),
]
