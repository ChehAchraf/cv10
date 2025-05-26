from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'password', 'is_premium', 'credits']

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Set credits based on premium status
        if validated_data.get('is_premium', False):
            validated_data['credits'] = 1
        else:
            validated_data['credits'] = 0
            
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            # Try to find the user directly first
            try:
                user = CustomUser.objects.get(email=email)
                # Check password manually
                if user.check_password(password):
                    # User exists and password is correct
                    if not user.is_active:
                        raise serializers.ValidationError('User account is disabled.')
                    data['user'] = user
                    return data
                else:
                    # Password is incorrect
                    raise serializers.ValidationError('Incorrect password.')
            except CustomUser.DoesNotExist:
                # User with this email doesn't exist
                raise serializers.ValidationError('No user found with this email address.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
