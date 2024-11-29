
# models.py
from django.db import models

class Laboratory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Computer(models.Model):
    name = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=17, unique=True)
    laboratory = models.ForeignKey(Laboratory, related_name='computers', on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('blocked', 'Bloccato'),
        ('unblocked', 'Sbloccato'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unblocked')


    def __str__(self):
        return f"{self.name} ({self.mac_address})"

