from django.db import models

class DICOMUpload(models.Model):
    patient_name = models.CharField(max_length=100)
    dicom_file = models.FileField(upload_to='dicom_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.dicom_file.name}"

