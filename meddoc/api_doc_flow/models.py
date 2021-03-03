from django.db import models
from django.core.exceptions import ValidationError
from rest_framework.serializers import ValidationError as SerializerValidationError


class Patient(models.Model):
    SEX = {
        (1, 'Male'),
        (2, 'Female'),
    }
    fio = models.CharField(max_length=256, null=False, blank=False)
    date_birth = models.DateField(null=False)
    sex = models.IntegerField(choices=SEX)


    def __str__(self):
        return self.fio

class Treatment(models.Model):
    RESULTS = {
        (1, 'Start'),
        (2, 'In progress'),
        (3, 'Done'),
    }
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    date_start = models.DateField(null=False, blank=False)
    date_finish = models.DateField(null=True, blank=True)
    result = models.IntegerField(choices=RESULTS, null=True, blank=True)

    def __str__(self):
        return 'Treatment for %s' % (self.patient)

class Document(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, blank=False)
    treatment = models.ForeignKey(Treatment, related_name='documents', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=256, null=False, blank=False)
    date = models.DateField(blank=False)

    def clean(self):
        if self.treatment:
            if self.treatment not in self.patient.treatment_set.all():
                raise SerializerValidationError('Patient cant be different')
                #raise ValidationError('Patient cant be different')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return '%s,  %s' % (self.title, self.patient.fio)

class DocumentBody(models.Model):
    document = models.OneToOneField(Document, primary_key=True, related_name='body', on_delete=models.CASCADE)
    body = models.JSONField()

    def __str__(self):
        return str(self.document)


