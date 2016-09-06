from django.db import models
from django.forms.models import modelform_factory

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
