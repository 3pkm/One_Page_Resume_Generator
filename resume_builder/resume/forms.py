from django import forms
from django.core.exceptions import ValidationError
from .models import Resume
import json

class ResumeForm(forms.ModelForm):
    # Education fields (will be converted to JSON)
    education_institution = forms.CharField(label="Institution Name", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    education_degree = forms.CharField(label="Degree/Diploma", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    education_field = forms.CharField(label="Field of Study", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    education_start_date = forms.CharField(label="Start Date", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YYYY'}))
    education_end_date = forms.CharField(label="End Date (or Expected)", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YYYY'}))
    education_gpa = forms.CharField(label="GPA", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    # Experience fields (will be converted to JSON)
    experience_company = forms.CharField(label="Company Name", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    experience_position = forms.CharField(label="Position", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    experience_location = forms.CharField(label="Location", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    experience_start_date = forms.CharField(label="Start Date", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YYYY'}))
    experience_end_date = forms.CharField(label="End Date (or Present)", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YYYY or Present'}))
    experience_description = forms.CharField(label="Description", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    
    # References fields (will be converted to JSON)
    reference_name = forms.CharField(label="Reference Name", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    reference_position = forms.CharField(label="Reference Position", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    reference_company = forms.CharField(label="Company", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    reference_email = forms.CharField(label="Email", required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    reference_phone = forms.CharField(label="Phone", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Resume
        fields = ['name', 'email', 'phone', 'location', 'linkedin', 'github', 'portfolio', 'objective', 
                 'courses', 'skills', 'certifications', 'achievements', 'leadership', 'languages']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g., john.doe@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., +1 234 567 8901'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., New York, NY'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'e.g., https://linkedin.com/in/johndoe'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'e.g., https://github.com/johndoe'}),
            'portfolio': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'e.g., https://johndoe.com'}),
            'objective': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'courses': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Data Structures, Algorithms, Web Development'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Python, JavaScript, Project Management'}),
            'certifications': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., AWS Certified Developer, PMP'}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'leadership': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., English (Native), Spanish (Intermediate)'}),
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Process education data
        education_data = {}
        if any([
            self.cleaned_data.get('education_institution'),
            self.cleaned_data.get('education_degree'),
            self.cleaned_data.get('education_field'),
        ]):
            education_data = {
                'institution': self.cleaned_data.get('education_institution', ''),
                'degree': self.cleaned_data.get('education_degree', ''),
                'field': self.cleaned_data.get('education_field', ''),
                'start_date': self.cleaned_data.get('education_start_date', ''),
                'end_date': self.cleaned_data.get('education_end_date', ''),
                'gpa': self.cleaned_data.get('education_gpa', ''),
            }
            instance.education = [education_data] if any(education_data.values()) else []
        
        # Process experience data
        experience_data = {}
        if any([
            self.cleaned_data.get('experience_company'),
            self.cleaned_data.get('experience_position'),
        ]):
            experience_data = {
                'company': self.cleaned_data.get('experience_company', ''),
                'position': self.cleaned_data.get('experience_position', ''),
                'location': self.cleaned_data.get('experience_location', ''),
                'start_date': self.cleaned_data.get('experience_start_date', ''),
                'end_date': self.cleaned_data.get('experience_end_date', ''),
                'description': self.cleaned_data.get('experience_description', ''),
            }
            instance.experience = [experience_data] if any(experience_data.values()) else []
            
        # Process reference data
        reference_data = {}
        if any([
            self.cleaned_data.get('reference_name'),
            self.cleaned_data.get('reference_email'),
        ]):
            reference_data = {
                'name': self.cleaned_data.get('reference_name', ''),
                'position': self.cleaned_data.get('reference_position', ''),
                'company': self.cleaned_data.get('reference_company', ''),
                'email': self.cleaned_data.get('reference_email', ''),
                'phone': self.cleaned_data.get('reference_phone', ''),
            }
            instance.references = [reference_data] if any(reference_data.values()) else []
        
        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        
        # Process Education data
        education_data = []
        if any([
            cleaned_data.get('education_institution'),
            cleaned_data.get('education_degree')
        ]):
            education_entry = {
                'institution': cleaned_data.get('education_institution', ''),
                'degree': cleaned_data.get('education_degree', ''),
                'field': cleaned_data.get('education_field', ''),
                'start_date': cleaned_data.get('education_start_date', ''),
                'end_date': cleaned_data.get('education_end_date', ''),
                'gpa': cleaned_data.get('education_gpa', '')
            }
            education_data.append(education_entry)
        cleaned_data['education'] = education_data
        
        # Process Experience data
        experience_data = []
        if any([
            cleaned_data.get('experience_company'),
            cleaned_data.get('experience_position')
        ]):
            experience_entry = {
                'company': cleaned_data.get('experience_company', ''),
                'position': cleaned_data.get('experience_position', ''),
                'location': cleaned_data.get('experience_location', ''),
                'start_date': cleaned_data.get('experience_start_date', ''),
                'end_date': cleaned_data.get('experience_end_date', ''),
                'description': cleaned_data.get('experience_description', '')
            }
            experience_data.append(experience_entry)
        cleaned_data['experience'] = experience_data
        
        # Process References data
        reference_data = []
        if cleaned_data.get('reference_name'):
            reference_entry = {
                'name': cleaned_data.get('reference_name', ''),
                'position': cleaned_data.get('reference_position', ''),
                'company': cleaned_data.get('reference_company', ''),
                'email': cleaned_data.get('reference_email', ''),
                'phone': cleaned_data.get('reference_phone', '')
            }
            reference_data.append(reference_entry)
        cleaned_data['references'] = reference_data
        
        return cleaned_data
        
    def clean_projects(self):
        try:
            # Process projects from form data
            projects_data = self.data.getlist('project_heading')
            projects_desc = self.data.getlist('project_description')
            
            projects = []
            for i in range(len(projects_data)):
                if projects_data[i]:  # Only add if heading exists
                    projects.append({
                        'heading': projects_data[i],
                        'description': projects_desc[i] if i < len(projects_desc) else ''
                    })
            return projects
        except Exception as e:
            raise ValidationError(f"Error processing projects: {str(e)}")
