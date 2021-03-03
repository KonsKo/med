import django_filters
from .models import Patient, Treatment, Document


class PatientFilter(django_filters.FilterSet):
    class Meta:
        model = Patient
        fields = {
            'fio': ['icontains',],
            'id': ['exact',],
        }


class TreatmentFilter(django_filters.FilterSet):

    class Meta:
        model = Treatment
        fields = {
            'patient__fio': ['icontains',],
        }


class DocumentFilter(django_filters.FilterSet):

    class Meta:
        model = Document
        fields = {
            'patient__fio': ['icontains',],
            'treatment': ['exact',],
        }