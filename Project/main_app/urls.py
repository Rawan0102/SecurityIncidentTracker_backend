from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import Home, RegisterView, ProfileListCreateView, ProfileDetailView, MyProfileView, IncidentListCreateView, IncidentDetailView, UserListView, CustomLoginView, ReportListCreateView, ReportDetailView, CommentListCreateView

urlpatterns = [
path('', Home.as_view(), name='home'),
path('api/register/', RegisterView.as_view(), name='register'),
path('api/token/', CustomLoginView.as_view(), name='token_obtain_pair'),  
path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
path('api/profiles/', ProfileListCreateView.as_view(), name='profile-list'),
path('api/profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
path('api/profiles/me/', MyProfileView.as_view(), name='my-profile'),
path('api/incidents/', IncidentListCreateView.as_view(), name='incident-list'),
path('api/incidents/<int:pk>/', IncidentDetailView.as_view(), name='incident-detail'),
path('api/users/', UserListView.as_view(), name='user-list'),
path('incidents/<int:incident_id>/reports/', ReportListCreateView.as_view(), name='report-list-create'),
path('reports/<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
path('reports/<int:report_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
]
