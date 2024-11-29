from django.contrib import admin

# Register your models here.
from .models import Laboratory,Computer
admin.site.register(Laboratory)
admin.site.register(Computer)