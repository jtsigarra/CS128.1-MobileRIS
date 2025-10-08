from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('upload_dicom/', views.upload_dicom, name='upload_dicom'),
    path('download_dicom/<int:dicom_id>/', views.download_dicom, name='download_dicom'),
]
