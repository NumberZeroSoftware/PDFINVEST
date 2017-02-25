from django import forms
from django.conf import settings

from .models import Document, Program

from datetime import date


class UploadFileForm(forms.ModelForm):
    
    class Meta:
        model = Document
        exclude = []


class ProgramForm(forms.ModelForm):
    
    class Meta:
        def years():
            return [i for i in range(date.today().year + settings.FUTURE_YEARS, 1968, -1)]

        model = Program
        fields = ('department', 'coordination', 'validity_trimester', 
                  'validity_year', 'denomination', 'code', 'credits', 
                  'requirements', 'theory_hours', 'practice_hours', 
                  'laboratory_hours', 'objectives', 'synoptic_content', 
                  'methodological_strategies', 'evaluation_strategies', 
                  'recommended_sources', )
        widgets = {
            'validity_year': forms.Select(choices=zip(years(), years()))
        }
