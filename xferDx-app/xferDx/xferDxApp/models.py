from django.db import models
import os
import uuid

class Patient(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('philhealth', 'PhilHealth'),
        ('hmo', 'HMO'),
    ]
    
    PROCEDURE_CHOICES = [
        ('xray', 'X-Ray'),
        ('ultrasound', 'Ultrasound'),
    ]
    
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    emergency_contact = models.CharField(max_length=20)
    physician_name = models.CharField(max_length=200)
    physician_email = models.EmailField()
    physician_phone = models.CharField(max_length=20)
    procedure_type = models.CharField(max_length=20, choices=PROCEDURE_CHOICES)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

def dicom_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex[:16]}.{ext}"
    return os.path.join('dicom_files', f'patient_{instance.patient.id}', unique_filename)

class DicomImage(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='dicom_images')
    file = models.FileField(upload_to=dicom_upload_path)
    study_id = models.CharField(max_length=100, unique=True, default="")
    exam_priority = models.CharField(max_length=50, choices=[
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('stat', 'Stat'),
    ], default='routine')
    clinical_history = models.TextField(blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    metadata_extracted = models.BooleanField(default=False)
    metadata = models.JSONField(blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True, help_text="File size in bytes")
    file_name = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.study_id:
            count = DicomImage.objects.count() + 1
            self.study_id = f"STUDY-{count:04d}"

        if self.file:
            self.file_name = self.file.name
            try:
                self.file_size = self.file.size
            except (ValueError, OSError):
                self.file_size = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"DICOM Study {self.study_id} for {self.patient.first_name} {self.patient.last_name}"

    class Meta:
        ordering = ['-upload_time']
