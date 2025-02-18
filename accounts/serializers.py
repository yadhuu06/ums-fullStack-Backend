from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(hello)
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)  
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)  # Display username
    email = serializers.EmailField(source="user.email")  # Allow updating email
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ["username", "email", "profile_image"]

    def update(self, instance, validated_data):
        # Update user email separately
        user_data = validated_data.pop("user", {})
        user = instance.user

        if "email" in user_data:
            user.email = user_data["email"]
            user.save()

        # Update profile image
        if "profile_image" in validated_data:
            instance.profile_image = validated_data["profile_image"]

        instance.save()
        return instance