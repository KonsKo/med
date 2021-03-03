from django.urls import path
from .views import *

urlpatterns = [
    path('get_patient_list/', PatientViewSet.as_view({'get': 'list'})),
    path('patient/<int:pk>/', PatientViewSet.as_view({'get': 'retrieve'})),
    path('patient/new/', PatientViewSet.as_view({'post': 'create'})),


    path('get_treatment_list/', TreatmentViewSet.as_view({'get': 'list'})),
    path('treatment/<int:pk>/', TreatmentViewSet.as_view({'get': 'retrieve'})),
    path('treatment/new/', TreatmentViewSet.as_view({'post': 'create'})),

    path('get_document_list/', DocumentViewSet.as_view({'get': 'list'})),
    path('document/<int:pk>/', DocumentViewSet.as_view({'get': 'retrieve'})),
    path('document/new/', DocumentViewSet.as_view({'post': 'create'})),

]