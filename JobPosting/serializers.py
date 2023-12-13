
from rest_framework import serializers
from .models import *


class CompanySocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySocialLink
        fields = ['social_name', 'social_link']


class CompanySerializer(serializers.ModelSerializer):
    social_links = CompanySocialLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'website', 'logo', 'country',
        'city', 'employee_number_range', 'social_links']
        

class JobSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkill
        fields = ['name']


class JobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = ['name']


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['name']


class FreelancerSocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerSocialLink
        fields = ['social_name', 'social_link']


class FreelancerProfileSerializer(serializers.ModelSerializer):
    skills = JobSkillSerializer(many=True, required=False)
    social_links = FreelancerSocialLinkSerializer(many=True, required=False)

    class Meta:
        model = FreelancerProfile
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only':True},
        }


class JobOpeningSerializer(serializers.ModelSerializer):
    required_skills = JobSkillSerializer(many=True, read_only=True)

    class Meta:
        model = JobOpening
        fields = '__all__'
        extra_kwargs = {
            'featured': {'required':False}
        }

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
        extra_kwargs = {
            'applicant': {'read_only':True}
        }


class JobRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRating
        fields = ['value', 'user', 'job_opening']


class JobReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobReview
        fields = ['user', 'job', 'comment']
        


