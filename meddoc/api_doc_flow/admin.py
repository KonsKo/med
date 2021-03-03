from django.contrib import admin
from .models import *

admin.site.register(Patient)
admin.site.register(Treatment)
admin.site.register(Document)
admin.site.register(DocumentBody)



