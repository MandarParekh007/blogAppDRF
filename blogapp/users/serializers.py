from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','password','phone','picture','bio']
    
    def create(self, validated_data):
        """
        Override the create method to handle password hashing.
        """
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Hash the password before saving
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Override the update method to handle password updates.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Hash the new password
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()