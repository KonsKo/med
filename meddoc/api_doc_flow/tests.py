from rest_framework import status
from rest_framework.test import APITestCase

import datetime

from .models import Patient, Treatment, Document, DocumentBody

class PatientViewSetTest(APITestCase):
    def setUp(self):
        self.patient1 = Patient.objects.create(
            fio='fio',
            date_birth=datetime.datetime.strptime('26 Sep 2012', '%d %b %Y'),
            sex=1
        )
        self.patient2 = Patient.objects.create(
            fio='fio2',
            date_birth=datetime.datetime.strptime('2 Sep 2002', '%d %b %Y'),
            sex=1
        )
        self.treatment1 = Treatment.objects.create(
            patient=self.patient1,
            date_start=datetime.datetime.strptime('26 Sep 2020', '%d %b %Y'),
            result=1
        )
        self.treatment2 = Treatment.objects.create(
            patient=self.patient2,
            date_start=datetime.datetime.strptime('26 Sep 2010', '%d %b %Y'),
            result=2
        )
        self.document1 = Document.objects.create(
            patient=self.patient1,
            treatment=self.treatment1,
            title='title1',
            date=datetime.datetime.strptime('26 Sep 2007', '%d %b %Y')
        )
        self.document2 = Document.objects.create(
            patient=self.patient2,
            title='title2',
            date=datetime.datetime.strptime('26 Sep 2008', '%d %b %Y')
        )
        self.body1 = DocumentBody.objects.create(
            document=self.document1,
            body='{ "name":"fio", "age":100000 }'
        )


    #PatientViewSet
    def test_PatientViewSet_get_patient_list(self):
        response = self.client.get('/api/get_patient_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        response = self.client.get('/api/get_patient_list/?fio__icontains=zzz')
        self.assertEqual(len(response.data), 0)
        response = self.client.get('/api/get_patient_list/?fio__icontains=io')
        self.assertEqual(len(response.data), 2)

    def test_PatientViewSet_get_exact_patient(self):
        response = self.client.get('/api/patient/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/patient/10/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_PatientViewSet_create_patient(self):
        date_birth = datetime.datetime.strptime('26 Sep 1990', '%d %b %Y').date()
        data = {'fio':'newfio', 'date_birth':date_birth, 'sex':'1'}
        response = self.client.post('/api/patient/new/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test with broken data for fio and date_birth
        date_birth = datetime.datetime.strptime('26 Sep 2030', '%d %b %Y').date()
        data = {'fio': 'newf7io', 'date_birth': date_birth, 'sex': '1'}
        response = self.client.post('/api/patient/new/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Date of birth must be les current date', response.data['date_birth'])
        self.assertIn('There is(are) wrong symbol(s) in fio: %s' % (['7',]), response.data['fio'])

    #TreatmentViewSet
    def test_TreatmentViewSet_get_treatment_list(self):
        response = self.client.get('/api/get_treatment_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('documents', response.data[0].keys())

        response = self.client.get('/api/get_treatment_list/?patient__fio__icontains=fio')
        self.assertEqual(len(response.data), 2)
        response = self.client.get('/api/get_treatment_list/?patient__fio__icontains=fio2')
        self.assertEqual(len(response.data), 1)

    def test_TreatmentViewSet_get_exact_treatment(self):
        response = self.client.get('/api/treatment/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('documents', response.data.keys())
        self.assertNotIn(self.body1.body, response.data.values())

    def test_TreatmentViewSet_create_treatment(self):
        date_start = datetime.datetime.strptime('26 Sep 2010', '%d %b %Y').date()
        date_finish = datetime.datetime.strptime('26 Sep 2020', '%d %b %Y').date()
        data = {'patient': self.patient1.id, 'date_start': date_start, 'result': '1', "date_finish": date_finish}
        response = self.client.post('/api/treatment/new/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #test with wrong data
        data = {'patient': self.patient1.id, 'date_start': date_finish, 'result': '1', "date_finish": date_start}
        response = self.client.post('/api/treatment/new/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date finish must be after date start', response.data['non_field_errors'])

    #DocumentViewSet
    def test_DocumentViewSet_get_document_list(self):
        response = self.client.get('/api/get_document_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('body', response.data[0].keys())

        response = self.client.get('/api/get_document_list/?patient__fio__icontains=2')
        self.assertEqual(len(response.data), 1)
        response = self.client.get('/api/get_document_list/?treatment=1')
        self.assertEqual(len(response.data), 1)
        response = self.client.get('/api/get_document_list/?treatment=2')
        self.assertEqual(len(response.data), 0)

    def test_TreatmentViewSet_get_exact_document(self):
        response = self.client.get('/api/document/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('body', response.data.keys())
        self.assertIn(self.body1.body, response.data['body']['body'])

    def test_DocumentViewSet_create_document(self):
        date = datetime.datetime.strptime('26 Sep 2010', '%d %b %Y').date()
        data = {'title': 'newtitle',
                'patient': self.patient1.id,
                'date': date,
                'treatment': self.treatment1.id,
                'body': {"body":"{ 'name':'test', 'age':1 }"}
                }
        qbody=len(DocumentBody.objects.all())
        response = self.client.post('/api/document/new/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(qbody+1, len(DocumentBody.objects.all()))

        data = {'title': 'newtitle',
               'patient': self.patient1.id,
               'date': date,
               'treatment': self.treatment2.id,
               'body': {"body": "{ 'name':'test', 'age':1 }"}
               }
        response = self.client.post('/api/document/new/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Patient cant be different', response.data)







