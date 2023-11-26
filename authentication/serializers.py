from rest_framework import serializers
from authentication.models import User
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