from django import forms
from .models import Document, Program
from datetime import date


class UploadFileForm(forms.ModelForm):
    
    class Meta:
        model = Document
        exclude = []


class ProgramForm(forms.ModelForm):
    
    class Meta:
        def years():
            return [i for i in range(date.today().year, 1968, -1)]

        model = Program
        fields = ('department', 'code', 'validity_trimester', 'validity_year',
                  'objectives', )
        widgets = {
            'validity_year': forms.Select(choices=zip(years(), years()))
        }
