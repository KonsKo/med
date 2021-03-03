# med
DRF app
<h5>Instruction:<h5>
<p> /api/get_patient_list/ - get list of patients, filters available by 'fio' and 'id' (example '/api/get_patient_list/?fio__icontains=test')</p>
<p> /api/patient/{id}/  - get patient instance by 'id'</p>
<p> /api/patient/new/ - create new patient, parameters {"fio"(digits and symbols +,=,(,), not available),
"date_birth"(less current date), 
"sex"(code 1-male, 2-female)} </p>
<p>/api/get_treatment_list/ - get list of treatments, filter available by 'fio' of patient (example '/api/get_treatment_list/?patient__fio__icontains=test')</p>
<p>/api/treatment/{id}/ - get treatment instance by 'id' with 'documents'(if exist) </p>
<p>/api/treatment/new/ - create new treatment, parameters {"date_start"(less current date),
"date_finish"(less date_start),
"result": (code 1-start, 2-in progress, 3-done),
"patient": exist patient instanse}</p>
<p>/api/get_document_list/ - get list of documents without body, filters available by 'fio' of patient and 'id' of treatment 
(example /api/get_document_list/?patient__fio__icontains=test, /api/get_document_list/?treatment=1)</p>
<p>/api/document/{id}/ - get document instance by 'id' with body, one document has one body</p>
<p>/api/document/new/ - create new document with body, parameters {"title" , "date"(less current date),
    "treatment"(treatment instance, not required),
    "patient"(patient instance, required)("treatment" has to connect with same "patient" as new document else raise error),
    "body":{"body"} (body of document in json)}</p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
<p></p>
