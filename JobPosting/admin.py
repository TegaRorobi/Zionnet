from django.contrib import admin
from .models import *

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company
    list_display = 'name', 'website', 'logo', 'employee_number_range'

@admin.register(CompanySocialLink)
class CompanySocialLinkAdmin(admin.ModelAdmin):
    model = CompanySocialLink
    list_display = 'company', 'social_name', 'social_link'

@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    model = FreelancerProfile
    list_display = 'user', 'title', '_skills', 'experience_range'

    @admin.display()
    def _skills(self, obj):
        return [skill.__str__() for skill in obj.skills.all()]

@admin.register(FreelancerSocialLink)
class FreelancerSocialLinkAdmin(admin.ModelAdmin):
    model = FreelancerSocialLink
    list_display = 'freelancer', 'social_name', 'social_link'

@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    model = JobOpening
    list_display = 'company', 'role', 'title', '_required_skills', 'category', 'experience_range'

    @admin.display()
    def _required_skills(self, obj):
        return [skill.__str__() for skill in obj.required_skills.all()]

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication
    list_display = 'applicant', 'job_opening', 'resume'

@admin.register(JobRating)
class JobRatingAdmin(admin.ModelAdmin):
    model = JobRating
    list_display = 'user', 'value', 'job_opening'

@admin.register(JobReview)
class JobReviewAdmin(admin.ModelAdmin):
    model = JobReview
    list_display = 'user', 'job', 'comment'

admin.site.register(JobSkill)
admin.site.register(JobRole)
admin.site.register(JobCategory)