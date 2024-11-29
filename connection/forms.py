# forms.py
from django import forms
from .models import Laboratory

class LaboratorySelectionForm(forms.Form):
    laboratory = forms.ModelChoiceField(queryset=Laboratory.objects.all(), label="Seleziona laboratorio")
