from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import Home, RegisterView 

urlpatterns = [
path('', Home.as_view(), name='home'),
path('api/register/', RegisterView.as_view(), name='register'),
path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]
