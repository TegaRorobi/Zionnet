from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from helpers.fields import ValidatedImageField, ValidatedResumeFileField
from helpers.models import TimestampsModel

User = get_user_model()


class Company(TimestampsModel):

    EMPLOYEE_NUMBER_CHOICES = [
        ('1-10', '1-10 Employees'),
        ('11-50', '11-50 Employees'),
        ('51-200', '51-200 Employees'),
        ('201-1000', '201-1000 Employees'),
        ('1000+', '1000+ Employees'),
    ]

    name = models.CharField(_('company name'), max_length=255)
    description = models.TextField(_('company description'), null=True, blank=True)
    website = models.URLField(_('company website'), null=True, blank=True)
    logo = ValidatedImageField(upload_to='job_posting/company/logos', null=True, blank=True)
    country = models.CharField(_('country'), max_length=255, null=True, blank=True)
    city = models.CharField(_('city'), max_length=255, null=True, blank=True)
    employee_number_range = models.CharField(
        _('employee number range'), choices=EMPLOYEE_NUMBER_CHOICES, max_length=20
    )

    def __str__(self):
        return self.name


class CompanySocialLink(TimestampsModel):

    SOCIAL_NAME_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('github', 'Github'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('behance', 'Behance'),
        ('dribble', 'Dribble'),
    ]

    company = models.ForeignKey(Company, related_name='social_links', on_delete=models.CASCADE)
    social_name = models.CharField(_('social name'), choices=SOCIAL_NAME_CHOICES, max_length=20)
    social_link = models.URLField(_('social link'))


class JobSkill(TimestampsModel):
    "Represents job skills like 'Figma', 'Django', 'Kubernetes'"
    name = models.CharField(_('skill name'), max_length=255)

    def __str__(self):
        return self.name


class JobRole(TimestampsModel):
    "Represents job roles like 'Developers', 'Product Managers'"
    name = models.CharField(_('role name'), max_length=255)

    def __str__(self):
        return self.name


class JobCategory(TimestampsModel):
    "Represents job categories like 'Business', 'Finance', 'Technology'"
    name = models.CharField(_('category name'), max_length=255)

    def __str__(self):
        return self.name


class FreelancerProfile(TimestampsModel):

    JOB_COMMITMENT_CHOICES = [
        ('part-time', 'Part Time'),
        ('full-time', 'Full Time'),
        ('contract', 'Contract'),
    ]
    JOB_PRESENCE_CHOICES = [
        ('remote', 'Remote'),
        ('on-site', 'On Site'),
        ('hybrid', 'Hybrid')
    ]
    EXPERIENCE_RANGE_CHOICES = [
        ('0-2', '0-2 years'),
        ('2-5', '2-5 years'),
        ('5-10', '5-10 years'),
        ('10-', '10+ years'),
    ]

    user = models.OneToOneField(User, related_name='freelancer_profile', on_delete=models.CASCADE)
    skills = models.ManyToManyField(JobSkill, related_name='freelancers')
    title = models.CharField(_('profile title'), max_length=255)
    bio = models.TextField(_('bio'), max_length=1535, null=True, blank=True)
    profile_pic = ValidatedImageField(
        upload_to='job_posting/freelancers/profile_images', extensions=('jpg', 'jpeg', 'png'), null=True, blank=True
    )
    banner_image = ValidatedImageField(
        upload_to='job_posting/freelancers/banner_images', extensions=('jpg', 'jpeg', 'png'), null=True, blank=True
    )
    resume = ValidatedResumeFileField(
        upload_to='job_posting/freelancers/resume_files', extensions=('pdf', 'docx'), null=True, blank=True
    )
    preferred_time_commitment = models.CharField(
        _('preferred time commitment'), choices=JOB_COMMITMENT_CHOICES, max_length=20, null=True, blank=True
    )
    preferred_presence_type = models.CharField(
        _('preferred job presence'), choices=JOB_PRESENCE_CHOICES, max_length=20, null=True, blank=True
    )
    experience_range = models.CharField(
        _('experience range (years)'), max_length=10, choices=EXPERIENCE_RANGE_CHOICES, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.title} - {self.user.__str__()}"


class FreelancerSocialLink(TimestampsModel):

    SOCIAL_NAME_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('github', 'Github'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('behance', 'Behance'),
        ('dribble', 'Dribble'),
    ]

    freelancer = models.ForeignKey(FreelancerProfile, related_name='social_links', on_delete=models.CASCADE)
    social_name = models.CharField(_('social name'), choices=SOCIAL_NAME_CHOICES, max_length=20)
    social_link = models.URLField(_('social link'))


class JobOpening(TimestampsModel):

    JOB_COMMITMENT_CHOICES = [
        ('part-time', 'Part Time'),
        ('full-time', 'Full Time'),
        ('contract', 'Contract'),
    ]
    JOB_PRESENCE_CHOICES = [
        ('remote', 'Remote'),
        ('on-site', 'On Site'),
        ('hybrid', 'Hybrid')
    ]
    EXPERIENCE_RANGE_CHOICES = [
        ('0-2', '0-2 years'),
        ('2-5', '2-5 years'),
        ('5-10', '5-10 years'),
        ('10-', '10+ years'),
    ]

    company = models.ForeignKey(
        Company, related_name='job_openings', on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        JobRole, verbose_name=_('job role'), related_name='jobs_openings', on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        JobCategory, verbose_name=_('job category'), related_name='job_openings', on_delete=models.CASCADE
    )
    poster = models.ForeignKey(
        User, related_name='posted_jobs', on_delete=models.SET_NULL, null=True # subject to deliberation
    )
    poster_positon = models.CharField(_('job poster position'), max_length=255, null=True, blank=True)
    title = models.CharField(_('job title'), max_length=511)
    description = models.TextField(_('job description'), null=True, blank=True)
    time_commitment = models.CharField(_('time commitment'), choices=JOB_COMMITMENT_CHOICES, max_length=20)
    presence_type = models.CharField(_('job presence'), choices=JOB_PRESENCE_CHOICES, max_length=20)
    experience_range = models.CharField(
        _('experience range (years)'), max_length=10, choices=EXPERIENCE_RANGE_CHOICES
    )
    required_skills = models.ManyToManyField(JobSkill, related_name='job_openings')
    resumption_date = models.DateField(_('resumption date'), null=True, blank=True)

    contract_period = models.DurationField(_('contract duration'), null=True, blank=True)
    hourly_rate = models.IntegerField(_('hourly rate'), null=True, blank=True)
    hourly_rate_currency = models.CharField(_('hourly rate currency'), max_length=1, default='$')


    def __str__(self):
        return self.title


class JobApplication(TimestampsModel):

    job_opening = models.ForeignKey(
        JobOpening, related_name='applications', on_delete=models.CASCADE
    )
    applicant = models.ForeignKey(
        FreelancerProfile, related_name='job_applications', on_delete=models.CASCADE
    )
    first_name = models.CharField(_('applicant\'s first name'), max_length=255)
    last_name = models.CharField(_('applicant\'s last name'), max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(_('applicant\'s phone number'), max_length=20, null=True, blank=True)
    application_info = models.CharField(_('applicant\'s other info'), max_length=512, null=True, blank=True)
    resume = ValidatedResumeFileField(
        upload_to='job_posting/freelancers/resume_files', extensions=('pdf', 'docx'), null=True, blank=True
    )


class JobRating(TimestampsModel):

    value = models.PositiveSmallIntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        User, related_name='job_ratings', on_delete=models.CASCADE
    )
    job_opening = models.ForeignKey(
        JobOpening, related_name='ratings', on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.job_opening.__str__()}: {self.value} stars"


class JobReview(TimestampsModel):
    user = models.ForeignKey(User, related_name='job_reviews', on_delete=models.CASCADE)
    job = models.ForeignKey(JobOpening, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField(_('review comment'), null=False, blank=False)

    def __str__(self):
        return f"{self.job.__str__()}: {self.user.__str__()}"

