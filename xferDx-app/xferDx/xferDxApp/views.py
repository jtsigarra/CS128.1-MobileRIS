from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PatientForm

# Home page view
def home(request):
    return render(request, 'home.html')

# View function to handle adding a new patient
def add_patient(request):
    # Check if the form was submitted (POST request)
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = PatientForm(request.POST)
        
        # Validate the form data
        if form.is_valid():
            # Save the patient to the database
            form.save()
            
            # Show a success message
            messages.success(request, 'Patient added successfully!')
            
            # Redirect back to the add patient page with a fresh form
            return redirect('add_patient')
        else:
            # If form is not valid, show error message
            messages.error(request, 'Please correct the errors below.')
    
    else:
        # If it's a GET request, create an empty form
        form = PatientForm()
    
    # Render the template with the form
    context = {
        'form': form,
    }
    return render(request, 'add_patient.html', context)