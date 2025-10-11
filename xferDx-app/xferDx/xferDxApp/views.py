from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PatientForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import PatientForm, DicomUploadForm
from .models import DicomImage, Patient
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import logout
import os

class CustomLoginView(LoginView):
    template_name = 'login.html'

def logout_view(request):
    logout(request)  # This clears the session and authentication
    return redirect('login')

@login_required
def dashboard(request):
    patients = Patient.objects.all()
    return render(request, 'dashboard.html', {
        'patients': patients,
    })

@login_required
def patient(request):
    patients = Patient.objects.all()
    return render(request, 'patient.html', {
        'patients': patients,
    })

@login_required
def telehealth(request):
    return render(request, 'telehealth.html')

@login_required
def dicom_upload(request):
    return render(request, 'dicom_upload.html')

@login_required
def reports(request):
    return render(request, 'reports.html')

@login_required
def add_patient(request):
    # Check if the form was submitted (POST request)
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = PatientForm(request.POST)
        
        # Validate the form data
        if form.is_valid():
            # Save the patient to the database
            form.save()
            
            # Show a success message
            messages.success(request, 'Patient added successfully!')
            
            # Redirect back to the add patient page with a fresh form
            return redirect('add_patient')
        else:
            # If form is not valid, show error message
            messages.error(request, 'Please correct the errors below.')
    
    else:
        # If it's a GET request, create an empty form
        form = PatientForm()
    
    # Render the template with the form
    context = {
        'form': form,
    }
    return render(request, 'add_patient.html', context)

def get_ph_time():
    """Get current time in Philippine timezone"""
    return timezone.now()

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