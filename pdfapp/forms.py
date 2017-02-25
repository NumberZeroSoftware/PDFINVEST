from django import forms
from django.conf import settings

from .models import Document, Program, Division

from datetime import date


class UploadFileForm(forms.ModelForm):
    
    class Meta:
        model = Document
        exclude = []


class ProgramForm(forms.ModelForm):
    division = forms.ModelChoiceField(
        label=u'División',
        queryset=Division.objects.all(),
        required=False
    )
    code = forms.CharField(min_length=1, max_length=10, 
                            strip=True, required=True,
                            label=Program._meta.get_field('code').verbose_name)
    denomination = forms.CharField(min_length=1, max_length=60, 
                                strip=True, required=True,
                                label=Program._meta.get_field('denomination').verbose_name)

    class Meta:
        def years():
            return [i for i in range(date.today().year + settings.FUTURE_YEARS, 1968, -1)]

        model = Program
        fields = ('division', 'department', 'coordination', 'validity_trimester', 
                  'validity_year', 'denomination', 'code', 'credits', 
                  'requirements', 'theory_hours', 'practice_hours', 
                  'laboratory_hours', 'objectives', 'synoptic_content', 
                  'methodological_strategies', 'evaluation_strategies', 
                  'recommended_sources', )
        widgets = {
            'validity_year': forms.Select(choices=zip(years(), years())), 
            'division': forms.ModelChoiceField(
                            label=u'División',
                            queryset=Division.objects.all(),
                            required=False
                            ),
        }
