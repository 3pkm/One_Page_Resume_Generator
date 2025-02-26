from django.db import models
from django.core.validators import RegexValidator

class Resume(models.Model):
    # Personal Information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)
    location = models.CharField(max_length=100)
    
    # Online Presence
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn Profile")
    github = models.URLField(blank=True, verbose_name="GitHub Profile")
    portfolio = models.URLField(blank=True, verbose_name="Portfolio Website")
    
    # Career Information
    objective = models.TextField(verbose_name="Career Objective")
    
    # Education
    education = models.JSONField(blank=True, default=list, verbose_name="Education History")
    
    # Skills and Courses
    courses = models.TextField(blank=True, help_text="Comma-separated list of relevant courses")
    skills = models.TextField(blank=True, help_text="Comma-separated list of skills")
    
    # Projects and Experience
    projects = models.JSONField(blank=True, default=list)
    experience = models.JSONField(blank=True, default=list, verbose_name="Work Experience")
    
    # Additional Information
    certifications = models.TextField(blank=True, help_text="Comma-separated list of certifications")
    achievements = models.TextField(blank=True)
    leadership = models.TextField(blank=True)
    languages = models.TextField(blank=True, help_text="Languages you speak with proficiency levels")
    
    # References
    references = models.JSONField(blank=True, default=list)
    
    # Resume Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
