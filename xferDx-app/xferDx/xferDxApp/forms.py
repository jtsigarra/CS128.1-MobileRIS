from django import forms
from .models import Patient

# Form for adding new patients
class PatientForm(forms.ModelForm):
    # Meta class tells Django which model to use and which fields to include
    class Meta:
        model = Patient  # Use the Patient model we created
        fields = [
            'first_name',
            'middle_name', 
            'last_name',
            'date_of_birth',
            'phone_number',
            'email_address',
            'emergency_contact',
            'physician_name',
            'physician_email',
            'physician_phone',
            'procedure_type',
            'scheduled_date',
            'scheduled_time',
            'payment_mode',
        ]
        
        # Widgets - customize how form fields look in HTML
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter middle name (optional)'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 09123456789'
            }),
            'email_address': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'patient@example.com'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact number'
            }),
            'physician_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter physician's name"
            }),
            'physician_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'doctor@example.com'
            }),
            'physician_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Physician's phone number"
            }),
            'procedure_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'scheduled_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'scheduled_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'payment_mode': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        
        # Custom labels for better readability
        labels = {
            'date_of_birth': 'Date of Birth',
            'physician_name': 'Primary Physician Name',
            'physician_email': 'Physician Email',
            'physician_phone': 'Physician Phone Number',
            'procedure_type': 'Procedure Type',
            'scheduled_date': 'Scheduled Date',
            'scheduled_time': 'Scheduled Time',
            'payment_mode': 'Payment Mode',
        }

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