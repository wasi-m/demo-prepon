from django.db import models

# Create your models here.

class Student(models.Model):
    batch = models.CharField(max_length=5)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, primary_key=True)
    contact = models.IntegerField()