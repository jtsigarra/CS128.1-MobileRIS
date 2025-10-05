from django.shortcuts import render, redirect
from .forms import DICOMUploadForm

def home(request):
    return render(request, 'home.html')

def upload_dicom(request):
    if request.method == 'POST':
        form = DICOMUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')
    else:
        form = DICOMUploadForm()
    return render(request, 'upload_dicom.html', {'form': form})

def upload_success(request):
    return render(request, 'upload_success.html')
