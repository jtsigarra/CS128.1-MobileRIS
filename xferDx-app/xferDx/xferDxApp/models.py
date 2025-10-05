from django.db import models

# Patient Model - stores all patient information
class Patient(models.Model):
    # Payment mode choices
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('philhealth', 'PhilHealth'),
        ('hmo', 'HMO'),
    ]
    
    # Procedure type choices (starting with X-ray and Ultrasound as mentioned in notes)
    PROCEDURE_CHOICES = [
        ('xray', 'X-Ray'),
        ('ultrasound', 'Ultrasound'),
    ]
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)  # blank=True means it's optional
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    
    # Contact Information
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    emergency_contact = models.CharField(max_length=20)
    
    # Primary Physician Information
    physician_name = models.CharField(max_length=200)
    physician_email = models.EmailField()
    physician_phone = models.CharField(max_length=20)
    
    # Procedure Information
    procedure_type = models.CharField(max_length=20, choices=PROCEDURE_CHOICES)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    
    # Automatic timestamps - Django will automatically set these
    created_at = models.DateTimeField(auto_now_add=True)  # Set when patient is first created
    updated_at = models.DateTimeField(auto_now=True)  # Updated every time patient info is changed
    
    # This method returns how the patient will be displayed in Django admin
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    # Meta class for additional options
    class Meta:
        ordering = ['-created_at']  # Newest patients first
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'