from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, permissions
from .models import Profile, Incident, Report, Comment
from .serializers import RegisterSerializer, ProfileSerializer, IncidentSerializer, UserSerializer, CustomTokenObtainPairSerializer, ReportSerializer, CommentSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import PermissionDenied


class ProfileListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class Home(APIView):
    def get(self, request):
        content = {'message': '...'}
        return Response(content)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyProfileView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        print("Reached MyProfileView")
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=404)

        
class IncidentListCreateView(generics.ListCreateAPIView):
    # queryset = Incident.objects.all().order_by('-created_at')
    def get_queryset(self):
        # return Incident.objects.filter(reporter=self.request.user).order_by('-created_at')
        return Incident.objects.all().order_by('-created_at')
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

class IncidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Incident.objects.filter(reporter=self.request.user)
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ReportListCreateView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        incident_id = self.request.query_params.get('incident_id')  

        if user.profile.role == 'manager':
            if incident_id:
                return Report.objects.filter(incident=incident_id)
            return Report.objects.all()
        
       
        if incident_id:
            return Report.objects.filter(author=user, incident=incident_id)
        return Report.objects.filter(author=user)

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
    #     if not serializer.is_valid():
    #         print(serializer.errors)
    #     serializer.save(author=self.request.user)



    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Validation Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profile.role == 'manager':
            return Report.objects.all()
        return Report.objects.filter(author=user)

    def perform_update(self, serializer):
        if self.request.user.profile.role != 'employee':
            raise PermissionDenied("Only employees can update reports.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.profile.role != 'employee':
            raise PermissionDenied("Only employees can delete reports.")
        instance.delete()

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(report_id=self.kwargs.get('report_id'))

    def perform_create(self, serializer):
        if self.request.user.profile.role != 'manager':
            raise PermissionDenied("Only managers can comment on reports.")
        serializer.save(author=self.request.user, report_id=self.kwargs.get('report_id'))