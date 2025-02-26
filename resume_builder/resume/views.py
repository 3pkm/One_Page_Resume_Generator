from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .forms import ResumeForm
from .models import Resume
import json

def resume_list(request):
    """View to display a list of all created resumes"""
    resumes = Resume.objects.all().order_by('-created_at')
    return render(request, 'resume_list.html', {'resumes': resumes})

def resume_form_view(request):
    """View to handle the resume creation form"""
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            
            # Process projects data
            projects = []
            project_headings = request.POST.getlist('project_heading')
            project_descriptions = request.POST.getlist('project_description')
            
            for i in range(len(project_headings)):
                if project_headings[i].strip():  # Only add if heading exists
                    projects.append({
                        'heading': project_headings[i],
                        'description': project_descriptions[i] if i < len(project_descriptions) else ''
                    })
            
            resume.projects = projects
            resume.save()
            
            messages.success(request, "Your resume has been created successfully!")
            return redirect('resume_display', resume_id=resume.id)
        else:
            messages.error(request, "There was an error with your form. Please check and try again.")
    else:
        form = ResumeForm()
    
    return render(request, 'resume_form.html', {'form': form})

def resume_form_display(request, resume_id=None):
    """View to display a resume by ID, or the latest if none specified"""
    if resume_id:
        resume = get_object_or_404(Resume, id=resume_id)
    else:
        resume = Resume.objects.last()
        if not resume:
            messages.error(request, "No resumes found. Please create one first.")
            return redirect('resume_form')
    
    # Process fields into lists for template
    courses = [course.strip() for course in resume.courses.split(',')] if resume.courses else []
    skills = [skill.strip() for skill in resume.skills.split(',')] if resume.skills else []
    certifications = [cert.strip() for cert in resume.certifications.split(',')] if resume.certifications else []
    languages = [lang.strip() for lang in resume.languages.split(',')] if resume.languages else []
    
    # Education and experience are already JSON fields
    education = resume.education
    experience = resume.experience
    projects = resume.projects
    references = resume.references

    return render(request, 'resume_display.html', {
        'resume': resume,
        'courses': courses,
        'skills': skills,
        'certifications': certifications,
        'languages': languages,
        'education': education,
        'experience': experience,
        'projects': projects,
        'references': references
    })

def edit_resume(request, resume_id):
    """View to edit an existing resume"""
    resume = get_object_or_404(Resume, id=resume_id)
    
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            updated_resume = form.save(commit=False)
            
            # Process projects data
            projects = []
            project_headings = request.POST.getlist('project_heading')
            project_descriptions = request.POST.getlist('project_description')
            
            for i in range(len(project_headings)):
                if project_headings[i].strip():  # Only add if heading exists
                    projects.append({
                        'heading': project_headings[i],
                        'description': project_descriptions[i] if i < len(project_descriptions) else ''
                    })
            
            updated_resume.projects = projects
            updated_resume.save()
            
            messages.success(request, "Resume updated successfully!")
            return redirect('resume_display', resume_id=resume.id)
    else:
        # Initialize form with current resume data
        form = ResumeForm(instance=resume)
        
        # Pre-populate education fields if data exists
        if resume.education and len(resume.education) > 0:
            education = resume.education[0]  # Get first education entry
            form.initial.update({
                'education_institution': education.get('institution', ''),
                'education_degree': education.get('degree', ''),
                'education_field': education.get('field', ''),
                'education_start_date': education.get('start_date', ''),
                'education_end_date': education.get('end_date', ''),
                'education_gpa': education.get('gpa', '')
            })
            
        # Pre-populate experience fields if data exists
        if resume.experience and len(resume.experience) > 0:
            experience = resume.experience[0]  # Get first experience entry
            form.initial.update({
                'experience_company': experience.get('company', ''),
                'experience_position': experience.get('position', ''),
                'experience_location': experience.get('location', ''),
                'experience_start_date': experience.get('start_date', ''),
                'experience_end_date': experience.get('end_date', ''),
                'experience_description': experience.get('description', '')
            })
            
        # Pre-populate reference fields if data exists
        if resume.references and len(resume.references) > 0:
            reference = resume.references[0]  # Get first reference entry
            form.initial.update({
                'reference_name': reference.get('name', ''),
                'reference_position': reference.get('position', ''),
                'reference_company': reference.get('company', ''),
                'reference_email': reference.get('email', ''),
                'reference_phone': reference.get('phone', '')
            })
    
    return render(request, 'resume_form.html', {'form': form, 'edit_mode': True, 'resume': resume})

def delete_resume(request, resume_id):
    """View to delete a resume"""
    resume = get_object_or_404(Resume, id=resume_id)
    
    if request.method == 'POST':
        resume.delete()
        messages.success(request, "Resume deleted successfully.")
        return redirect('resume_list')
        
    return render(request, 'delete_confirm.html', {'resume': resume})

def download_resume_pdf(request, resume_id):
    """View to download resume as PDF using ReportLab"""
    resume = get_object_or_404(Resume, id=resume_id)
    
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.name.replace(" ", "_")}_Resume.pdf"'
    
    # Create the PDF object using ReportLab
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                          rightMargin=72,
                          leftMargin=72,
                          topMargin=72,
                          bottomMargin=72)
    
    # Container for the "Flowable" objects
    elements = []
    
    # Get the default stylesheet
    styles = getSampleStyleSheet()
    
    # Modify existing Normal style
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 14
    styles['Normal'].spaceBefore = 6
    styles['Normal'].spaceAfter = 6
    
    # Add custom styles
    styles.add(ParagraphStyle(name='ResumeHeading',
                            fontSize=24,
                            leading=30,
                            textColor=colors.HexColor('#222222'),
                            spaceAfter=20))
    styles.add(ParagraphStyle(name='SectionHeading',
                            fontSize=14,
                            leading=20,
                            textColor=colors.HexColor('#444444'),
                            spaceBefore=15,
                            spaceAfter=10))
    styles.add(ParagraphStyle(name='Small',
                            fontSize=9,
                            leading=12))
    
    # Add name and contact info
    elements.append(Paragraph(resume.name, styles['ResumeHeading']))
    contact_info = [
        [Paragraph(f"Email: {resume.email}", styles['Small']),
         Paragraph(f"Phone: {resume.phone}", styles['Small'])],
        [Paragraph(f"Location: {resume.location}", styles['Small']),
         Paragraph(f"", styles['Small'])]  # Empty cell for alignment
    ]
    
    if resume.linkedin or resume.github or resume.portfolio:
        links = []
        if resume.linkedin:
            links.append(f"LinkedIn: {resume.linkedin}")
        if resume.github:
            links.append(f"GitHub: {resume.github}")
        if resume.portfolio:
            links.append(f"Portfolio: {resume.portfolio}")
        contact_info.append([Paragraph(", ".join(links), styles['Small'])])
    
    elements.append(Table(contact_info, colWidths=['50%', '50%']))
    elements.append(Spacer(1, 20))
    
    # Career Objective
    if resume.objective:
        elements.append(Paragraph("Career Objective", styles['SectionHeading']))
        elements.append(Paragraph(resume.objective, styles['Normal']))
    
    # Education
    if resume.education:
        elements.append(Paragraph("Education", styles['SectionHeading']))
        for edu in resume.education:
            elements.append(Paragraph(
                f"<b>{edu.get('degree')} in {edu.get('field')}</b><br/>"
                f"{edu.get('institution')}<br/>"
                f"{edu.get('start_date')} - {edu.get('end_date')}"
                + (f"<br/>GPA: {edu.get('gpa')}" if edu.get('gpa') else ""),
                styles['Normal']
            ))
    
    # Skills
    if resume.skills:
        elements.append(Paragraph("Skills", styles['SectionHeading']))
        elements.append(Paragraph(resume.skills, styles['Normal']))
    
    # Experience
    if resume.experience:
        elements.append(Paragraph("Work Experience", styles['SectionHeading']))
        for exp in resume.experience:
            elements.append(Paragraph(
                f"<b>{exp.get('position')}</b><br/>"
                f"{exp.get('company')} - {exp.get('location')}<br/>"
                f"{exp.get('start_date')} - {exp.get('end_date')}<br/>"
                f"{exp.get('description')}",
                styles['Normal']
            ))
    
    # Projects
    if resume.projects:
        elements.append(Paragraph("Projects", styles['SectionHeading']))
        for project in resume.projects:
            elements.append(Paragraph(
                f"<b>{project.get('heading')}</b>: {project.get('description')}",
                styles['Normal']
            ))
    
    # Leadership
    if resume.leadership:
        elements.append(Paragraph("Leadership", styles['SectionHeading']))
        elements.append(Paragraph(resume.leadership, styles['Normal']))
    
    # Achievements
    if resume.achievements:
        elements.append(Paragraph("Achievements", styles['SectionHeading']))
        elements.append(Paragraph(resume.achievements, styles['Normal']))
    
    # Certifications
    if resume.certifications:
        elements.append(Paragraph("Certifications", styles['SectionHeading']))
        elements.append(Paragraph(resume.certifications, styles['Normal']))
    
    # Languages
    if resume.languages:
        elements.append(Paragraph("Languages", styles['SectionHeading']))
        elements.append(Paragraph(resume.languages, styles['Normal']))
    
    # References
    if resume.references:
        elements.append(Paragraph("References", styles['SectionHeading']))
        for ref in resume.references:
            elements.append(Paragraph(
                f"<b>{ref.get('name')}</b><br/>"
                f"{ref.get('position')} at {ref.get('company')}<br/>"
                f"Email: {ref.get('email')}"
                + (f"<br/>Phone: {ref.get('phone')}" if ref.get('phone') else ""),
                styles['Normal']
            ))
    
    # Build the PDF document
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and return the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response
