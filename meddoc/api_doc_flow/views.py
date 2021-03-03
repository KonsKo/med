from rest_framework import generics
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend

from .models import Patient, Treatment, Document, DocumentBody
from .serializers import *
from .filters import PatientFilter, TreatmentFilter, DocumentFilter


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filterset_class = PatientFilter
    filter_backends = (DjangoFilterBackend,)
    search_fields = ['fio', 'id', ]


class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    filterset_class = TreatmentFilter
    filter_backends = (DjangoFilterBackend,)
    search_fields = ['patient_fio',]


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filterset_class = DocumentFilter
    filter_backends = (DjangoFilterBackend,)
    earch_fields = ['patient_fio', 'treatment',]












