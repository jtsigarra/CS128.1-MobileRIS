from django import forms
from .models import DICOMUpload

class DICOMUploadForm(forms.ModelForm):
    class Meta:
        model = DICOMUpload
        fields = ['patient_name', 'dicom_file']
