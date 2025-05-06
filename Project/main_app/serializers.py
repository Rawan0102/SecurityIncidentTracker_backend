from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Incident, Report, Comment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ReportSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    incident_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'incident', 'incident_id', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    report_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'report', 'report_id', 'author', 'author_username', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class IncidentSerializer(serializers.ModelSerializer):
    # reporter = serializers.ReadOnlyField(source='reporter.username')
    reports = ReportSerializer(many=True, read_only=True)
    resolved = serializers.BooleanField()

    class Meta:
        model = Incident
        fields = [
                'id','title','description','severity',
                'category','location','assigned',
                'created_at','updated_at','resolved','reporter', 'reports'
            ]
        read_only_fields = ['id','created_at','updated_at','resolved','reporter']
        assigned = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    # role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],  
            password=validated_data['password']
        )
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
   
        return token