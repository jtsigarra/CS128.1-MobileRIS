from django.contrib import admin
from .models import Patient, DicomImage

# Register your models here.
admin.site.register(Patient)

@admin.register(DicomImage)
class DicomImageAdmin(admin.ModelAdmin):
    list_display = ['study_id', 'patient', 'exam_priority', 'upload_time', 'metadata_extracted']
    list_filter = ['exam_priority', 'upload_time', 'metadata_extracted']
    search_fields = ['study_id', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['upload_time']