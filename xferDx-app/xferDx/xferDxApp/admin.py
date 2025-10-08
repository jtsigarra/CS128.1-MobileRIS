from django.contrib import admin
from .models import Patient, DicomImage

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'procedure_type', 'scheduled_date', 'created_at']
    list_filter = ['procedure_type', 'payment_mode', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone_number']

@admin.register(DicomImage)
class DicomImageAdmin(admin.ModelAdmin):
    list_display = ['study_id', 'patient', 'exam_priority', 'upload_time', 'metadata_extracted']
    list_filter = ['exam_priority', 'upload_time', 'metadata_extracted']
    search_fields = ['study_id', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['upload_time']
