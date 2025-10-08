from django.urls import path, include
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('patient/', views.patient, name='patient'),
    path('telehealth/', views.telehealth, name='telehealth'),
    path('reports/', views.reports, name='reports'),
    path('upload_dicom/', views.upload_dicom, name='upload_dicom'),
    path('download_dicom/<int:dicom_id>/', views.download_dicom, name='download_dicom'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)