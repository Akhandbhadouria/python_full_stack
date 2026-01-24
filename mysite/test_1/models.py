from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    reg=models.CharField(max_length=100)
    def __str__(self):
        return self.name
