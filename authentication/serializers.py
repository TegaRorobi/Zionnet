from rest_framework import serializers
from authentication.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length = 8, max_length = 68,
                                     write_only = True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'country', 'password']
        
    def validate(self, attrs):            
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)
    tokens = serializers.CharField(min_length=8, max_length=68, read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        return {
            'email': user.email,
            'tokens' : user.tokens()
        }
        