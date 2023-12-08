
from rest_framework import serializers
from .models import *


class FreelancerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerProfile
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only':True},
        }


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
        extra_kwargs = {
            'applicant': {'read_only':True}
        }

