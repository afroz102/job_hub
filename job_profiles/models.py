from django.db import models
from users.models import UserProfile
from django.contrib.auth.models import User


class Portfolio(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


# LANGUAGE_FLUENCY = (
#     ('0', 'Native'),
#     ('1', 'Fluent'),
#     ('2', 'Limited'),
#     ('3', 'Elementary'),
# )

class LanguageKnown(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    # fluency = models.CharField(max_length=50, choices=LANGUAGE_FLUENCY)
    fluency = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.language


class EducationDetail(models.Model):
    EDUCATION_QUALIFICATION = (
        ('0', 'Doctorate/PhD'),
        ('1', 'Masters/Post-Graduation'),
        ('2', 'Graduation/Diploma'),
        ('3', '12th'),
    )
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    education = models.CharField(
        max_length=100, choices=EDUCATION_QUALIFICATION, null=True)
    course = models.CharField(max_length=100, null=True)
    specialization = models.CharField(max_length=100, null=True)
    university = models.CharField(max_length=200, null=True)
    graduation_year = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.course


class Skill(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.skill


class PreferedLocation(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    prefered_location = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.prefered_location
