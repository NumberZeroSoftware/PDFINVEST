from django import forms
from .models import Document


class UploadFileForm(forms.ModelForm):
    
    class Meta:
        model = Document
        exclude = []
