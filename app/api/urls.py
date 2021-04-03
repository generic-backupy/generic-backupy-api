from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'pages', PageViewSet, basename="pages")
router.register(r'users', UserViewSet, basename="users")
router.register(r'push-tokens', PushTokenViewSet, basename="push-tokens")
router.register(r'tags', TagViewSet, basename="tags")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'api-auth/', include('knox.urls')),
    path('auth/', SignInAPI.as_view()),
    #path('auth/', obtain_auth_token, name='auth'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('username-available/', UsernameAvailableView.as_view(), name='username_available'),
    path('email-available/', EmailAvailableView.as_view(), name='email_available'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
