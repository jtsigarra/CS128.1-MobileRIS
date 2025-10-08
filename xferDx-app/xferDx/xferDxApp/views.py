from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PatientForm, DicomUploadForm
from .models import Patient, DicomImage
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime

def get_ph_time():
    """Get current time in Philippine timezone"""
    return timezone.now()

# Dashboard view
@login_required
def dashboard(request):
    patients = Patient.objects.all().order_by('-created_at')
    
    # Calculate statistics
    total_dicom_studies = DicomImage.objects.count()
    xray_count = patients.filter(procedure_type='xray').count()
    ultrasound_count = patients.filter(procedure_type='ultrasound').count()
    
    # Get recent DICOM studies (last 10)
    recent_dicom_studies = DicomImage.objects.all().order_by('-upload_time')[:10]
    
    context = {
        'patients': patients,
        'total_dicom_studies': total_dicom_studies,
        'xray_count': xray_count,
        'ultrasound_count': ultrasound_count,
        'recent_dicom_studies': recent_dicom_studies,
    }
    return render(request, 'dashboard.html', context)

# Add patient view
@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient added successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})

# DICOM upload view
@login_required
def upload_dicom(request):
    if request.method == 'POST':
        form = DicomUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('dicom_files')
        
        if form.is_valid():
            patient = form.cleaned_data['patient']
            exam_priority = form.cleaned_data['exam_priority']
            clinical_history = form.cleaned_data['clinical_history']

            # Create directory if it doesn't exist
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'dicom_files', f'patient_{patient.id}')
            os.makedirs(upload_dir, exist_ok=True)

            for f in files:
                # Create unique study ID
                import uuid
                study_id = f"STUDY-{uuid.uuid4().hex[:8].upper()}"
                
                # Save the file
                dicom_image = DicomImage(
                    patient=patient,
                    file=f,
                    study_id=study_id,
                    exam_priority=exam_priority,
                    clinical_history=clinical_history
                )
                dicom_image.save()
                
            messages.success(request, f'Successfully uploaded {len(files)} DICOM file(s)!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DicomUploadForm()
    
    return render(request, 'upload_dicom.html', {'form': form})

# Add download_dicom function
@login_required
def download_dicom(request, dicom_id):
    dicom_image = get_object_or_404(DicomImage, id=dicom_id)
    
    if dicom_image.file:
        try:
            with open(dicom_image.file.path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/dicom')
                response['Content-Disposition'] = f'attachment; filename="{dicom_image.file_name}"'
                return response
        except Exception as e:
            messages.error(request, f'Error downloading file: {str(e)}')
            return redirect('dashboard')
    else:
        messages.error(request, 'File not found')
        return redirect('dashboard')
