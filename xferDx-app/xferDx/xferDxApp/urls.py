from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for add patient page
    # When user goes to /add-patient/, it will call the add_patient view
    path('add-patient/', views.add_patient, name='add_patient'),
    
    # If you have a home URL pattern, add it here too
    path('', views.home, name='home'),
    
    # Add other URL patterns here as you build more features
]