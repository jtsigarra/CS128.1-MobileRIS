from django import forms
from .models import Patient

# Custom widget for multiple file uploads
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

# Form for adding new patients
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'middle_name', 'last_name', 'date_of_birth',
            'phone_number', 'email_address', 'emergency_contact',
            'physician_name', 'physician_email', 'physician_phone',
            'procedure_type', 'scheduled_date', 'scheduled_time', 'payment_mode'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'scheduled_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'scheduled_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['date_of_birth', 'scheduled_date', 'scheduled_time']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

# Form for uploading DICOM files
class DicomUploadForm(forms.Form):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Patient"
    )
    exam_priority = forms.ChoiceField(
        choices=[('routine','Routine'), ('urgent','Urgent'), ('stat','Stat')],
        widget=forms.Select(attrs={'class':'form-control'}),
        label="Exam Priority"
    )
    clinical_history = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class':'form-control', 'rows':3, 'placeholder': 'Enter clinical history and notes...'}),
        label="Clinical History"
    )
    # Use our custom multiple file field
    dicom_files = MultipleFileField(
        widget=MultipleFileInput(attrs={'class': 'form-control'}),
        help_text="Select one or more DICOM files (.dcm, .dicom) or compressed archives (.zip, .tar.gz)",
        label="DICOM Files"
    )
