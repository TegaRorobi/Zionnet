<<<<<<< HEAD

from rest_framework import serializers
from .models import *


class FreelancerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerProfile
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only':True},
        }

=======
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
    skills = JobSkillSerializer(many=True, read_only=True)
    social_links = FreelancerSocialLinkSerializer(many=True, read_only=True)

    class Meta:
        model = FreelancerProfile
        fields = ['id', 'user', 'skills', 'title', 'bio', 'profile_pic', 'banner_image', 'resume',
                  'preferred_time_commitment', 'preferred_presence_type', 'experience_range', 'social_links']

class JobOpeningSerializer(serializers.ModelSerializer):
    required_skills = JobSkillSerializer(many=True, read_only=True)

    class Meta:
        model = JobOpening
        fields = ['id', 'company', 'role', 'category', 'poster', 'poster_positon', 'title', 'description',
                  'time_commitment', 'presence_type', 'experience_range', 'required_skills', 'resumption_date',
                  'contract_period', 'hourly_rate', 'hourly_rate_currency']
>>>>>>> ee2d3c040ba3840553df8a6a3ed01dcfabaad546

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
<<<<<<< HEAD
        fields = '__all__'
        extra_kwargs = {
            'applicant': {'read_only':True}
        }

=======
        fields = ['id', 'job_opening', 'applicant', 'first_name', 'last_name', 'email', 'phone_number', 'application_info', 'resume']

class JobRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRating
        fields = ['value', 'user', 'job_opening']

class JobReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobReview
        fields = ['user', 'job', 'comment']
        
>>>>>>> ee2d3c040ba3840553df8a6a3ed01dcfabaad546
