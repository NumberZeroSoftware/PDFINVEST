from django import forms
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.forms.widgets import TextInput
from django.forms.utils import ErrorList

from .models import Document, Program, Division, Department

from datetime import date

# Custom Errors
class DivErrorList(ErrorList):
     def __str__(self):  
         return self.as_divs()
     def as_divs(self):
         if not self: return ''
         return format_html('<div class="errorlist">%s</div>' % ''.join(['<div class="error red-text">%s</div>' % e for e in self]))


# Custom widgets

# Using Jquery and chained plugin we get chained selects
class DepartmentChainedSelectWidget(forms.Select):
    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        # Lets see if we are selected
        if option_value in selected_choices:
            selected_html = mark_safe(u' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = u''
        department_reference = u''
        # We want to get the class of only valid options
        if option_value:
            # Get the associated department
            department_id = Department.objects.get(name=option_value).division
            return format_html(u'<option value="{0}"{1} class="{2}">{3}</option>',
                           option_value,
                           selected_html,
                           department_id,
                           force_text(option_label))
        else:
            return format_html(u'<option value="{0}"{1}{2}>{3}</option>',
                           option_value,
                           selected_html,
                           department_reference,
                           force_text(option_label))


# Forms

class UploadFileForm(forms.ModelForm):
    
    class Meta:
        model = Document
        exclude = []

class TextStringForm(forms.ModelForm):
    
    class Meta:
        model = Document
        exclude = ('date', 'docfile', 'ready_html', 'processing_html', 'file_name', 'file_path',)

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
        fields = ('code', 'denomination', 'validity_trimester', 'validity_year',
                  'theory_hours', 'practice_hours', 'laboratory_hours', 
                  'credits', 'requirements', 'objectives', 'synoptic_content',
                  'methodological_strategies', 'evaluation_strategies',
                  'recommended_sources',
                  'division', 'department', 'coordination', 
                   )
        widgets = {
            'validity_year': forms.Select(choices=zip([""]+years(), ["------"]+years())), 
            'division': forms.ModelChoiceField(
                            label=u'División',
                            queryset=Division.objects.all(),
                            required=False
                            ),
            'department': DepartmentChainedSelectWidget(),
            'code': TextInput(attrs={'class':'input-field  col s3'}),
            'denomination': TextInput(attrs={'class':'materialize-textarea'}),
            #'validity_year': TextInput(attrs={'class':'input-field'}),
            #'validity_trimester': TextInput(attrs={'class':'input-field'}),
            'theory_hours': TextInput(attrs={'class':'input-field'}),
            'practice_hours': TextInput(attrs={'class':'input-field'}),
            'laboratory_hours': TextInput(attrs={'class':'input-field'}),
            'credits': TextInput(attrs={'class':'input-field'}),
            'requirements': TextInput(attrs={'class':'input-field'}),
            'objectives': TextInput(attrs={'class':'input-field'}),
            'synoptic_content': TextInput(attrs={'class':'input-field'}),
            'methodological_strategies': TextInput(attrs={'class':'input-field'}),
            'evaluation_strategies': TextInput(attrs={'class':'input-field'}),
            'recommended_sources': TextInput(attrs={'class':'input-field'}),
            #'department': TextInput(attrs={'class':'input-field'}),
            'coordination': TextInput(attrs={'class':'input-field'}),
        }
