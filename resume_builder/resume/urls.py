from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume_list, name='resume_list'),
    path('new/', views.resume_form_view, name='resume_form'),
    path('display/<int:resume_id>/', views.resume_form_display, name='resume_display'),
    path('display/', views.resume_form_display, name='latest_resume'),
    path('edit/<int:resume_id>/', views.edit_resume, name='edit_resume'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('download/<int:resume_id>/', views.download_resume_pdf, name='download_resume_pdf'),
]
