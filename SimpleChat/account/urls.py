from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('api/register/', RegisterView.as_view(), name="sign_up"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]