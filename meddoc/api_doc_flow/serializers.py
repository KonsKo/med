from rest_framework import serializers
from rest_framework.serializers import ValidationError

import datetime
import re

from .models import Patient, Treatment, Document, DocumentBody


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def validate_date_birth(self, value):
        now = datetime.datetime.now().date()
        if value > now:
            raise ValidationError('Date of birth must be les current date')
        return value

    def validate_fio(self, value):
        pattern = '\d+|[\=\+\(\)]'
        mis = re.findall(pattern, value)
        if mis:
            raise ValidationError('There is(are) wrong symbol(s) in fio: %s' % (mis))
        return value


class TreatmentSerializer(serializers.ModelSerializer):
    patient_fio = serializers.CharField(source='patient.fio', read_only=True)
    documents = serializers.StringRelatedField(many=True)

    class Meta:
        model = Treatment
        fields = ['patient_fio', 'date_start', 'date_finish', 'result', 'documents', 'patient']

    def __init__(self, *args, **kwargs):
        if kwargs['context']['view'].action == 'list':
            del self.fields['documents']
            del self.fields['patient']
        if kwargs['context']['view'].action == 'retrieve':
            del self.fields['patient']
        if kwargs['context']['view'].action == 'create':
            del self.fields['patient_fio']
            del self.fields['documents']
        super().__init__(*args, **kwargs)

    def validate(self, data):
        date_start = data['date_start']
        now = datetime.datetime.now().date()
        if date_start > now:
            raise ValidationError('date start must be les current date')
        if data['date_finish']:
            if data['date_finish'] < date_start:
                raise ValidationError('date finish must be after date start')
        return data



class DocumentBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentBody
        fields = ['body']


class DocumentSerializer(serializers.ModelSerializer):
    patient_fio = serializers.CharField(source='patient.fio', read_only=True)
    body = DocumentBodySerializer()

    class Meta:
        model = Document
        fields = ['id','title', 'patient_fio', 'date', 'treatment', 'body', 'patient']

    def __init__(self, *args, **kwargs):
        if kwargs['context']['view'].action == 'list':
            del self.fields['body']
            del self.fields['patient']
        if kwargs['context']['view'].action == 'retrieve':
            del self.fields['patient']
            del self.fields['id']
        super().__init__(*args, **kwargs)

    def validate_date(self, value):
        now = datetime.datetime.now().date()
        if value > now:
            raise ValidationError('date must be les current date')
        return value


    def create(self, validated_data):
        title = validated_data['title']
        date = validated_data['date']
        treatment = validated_data['treatment']
        patient = validated_data['patient']
        document = Document.objects.create(title=title, date=date, treatment=treatment, patient=patient)
        body = DocumentBody.objects.create(document=document, body=validated_data.get('body')['body'])
        return document



