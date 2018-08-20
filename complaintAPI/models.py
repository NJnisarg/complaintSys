from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=32, null=False, unique=True, primary_key=True)


class Complaint(models.Model):
    complainant = models.CharField(null=False, max_length=32)
    respondent = models.CharField(null=True, max_length=32, default=None)
    title = models.CharField(max_length=256, null=False)
    description = models.TextField(null=False)
    status = models.BooleanField(default=False)
    tag = models.CharField(null=False, max_length=32)
    createdOn = models.DateField(auto_now=True)
    comment = models.TextField(null=True, default=None)
