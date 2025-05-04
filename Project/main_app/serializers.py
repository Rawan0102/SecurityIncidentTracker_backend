from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Incident

class IncidentSerializer(serializers.ModelSerializer):
    reporter = serializers.ReadOnlyField(source='reporter.username')

    class Meta:
        model = Incident
        fields = [
                'id','title','description','severity',
                'category','location',
                'created_at','updated_at','resolved','reporter'
            ]
        read_only_fields = ['id','created_at','updated_at','resolved','reporter']

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
    
