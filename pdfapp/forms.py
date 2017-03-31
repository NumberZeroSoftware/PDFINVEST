from django import forms
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.forms.widgets import TextInput, Textarea, Input, SelectMultiple, Select, HiddenInput
from django.forms.utils import ErrorList, flatatt


from .models import Document, Program, Division, Department, Coordination, Code, Programa, AdditionalName, Reference, Author

from datetime import date

# Custom Errors
class DivErrorList(ErrorList):
     def __str__(self):  
         return self.as_divs()
     def as_divs(self):
         if not self: return ''
         return format_html('<div class="errorlist longText">%s</div>' % ''.join(['<div class="error red-text longText">%s</div>' % e for e in self]))


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

# Materialize Range Field
# To understand how to overload go to:
# https://code.djangoproject.com/ticket/20674
# https://docs.djangoproject.com/en/1.10/_modules/django/forms/widgets/#Input (Look for Input, TextInput, NumberInput)
class NumberRangeFieldInput(Input):
    input_type = 'range'
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))
        return format_html('<p class="range-field"><input{} /></p>', flatatt(final_attrs))

    def __init__(self, range_min=0, range_max=100, step=1, attrs=None):
        if attrs is not None:
            self.input_type = attrs.pop('type', self.input_type)
        else:
            attrs = {}

        if not 'min' in attrs:
            attrs['min'] = str(range_min)

        if not 'max' in attrs:
            attrs['max'] = str(range_max)

        if not 'step' in attrs:
            attrs['step'] = str(step)

        super(NumberRangeFieldInput, self).__init__(attrs)

# Materialize Multiple Select
class SelectMultipleMaterialize(SelectMultiple):
    def render(self, name, value, attrs=None):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<select multiple{}>', flatatt(final_attrs))]
        options = self.render_options(value)
        output.append('<option value="" disabled selected>--------</option>')
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option value="{}"{}>{}</option>', option_value, selected_html, force_text(option_label))

# Materialize Select
class SelectMaterialize(Select):
    def render(self, name, value, attrs=None):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<select {}>', flatatt(final_attrs))]
        options = self.render_options(value)
        output.append('<option value="" disabled selected>--------</option>')
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option value="{}"{}>{}</option>', option_value, selected_html, force_text(option_label))

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

    denomination = forms.CharField(min_length=1, max_length=60, 
                                strip=True, required=True,
                                label=Program._meta.get_field('denomination').verbose_name)

    class Meta:
        def years():
            return [i for i in range(date.today().year + settings.FUTURE_YEARS, 1968, -1)]

        def days():
            return [i for i in range(1, 32)]

        def credits():
            return [i for i in range(0, 17)]

        def hours():
            return [i for i in range(0, 41)]

        model = Program
        fields = ('code', 'number', 'denomination', 'validity_trimester', 'validity_year',
                  'validity_date_y', 'validity_date_m', 'validity_date_d',
                  'theory_hours', 'practice_hours', 'laboratory_hours', 
                  'credits', 'requirements', 'objectives', 'synoptic_content', 
                  'methodological_strategies', 'evaluation_strategies',
                  'division', 'department', 'coordination', 'passes', 'specific_objectives'
                   )
        widgets = {
            'validity_year' : forms.Select(choices=zip([""]+years(), ["------"]+years())),
            'validity_date_y': forms.Select(choices=zip([""]+years(), ["------"]+years())),
            'validity_date_m': Select(),
            'validity_date_d': NumberRangeFieldInput(range_min=1, range_max=31),
            'division': forms.ModelChoiceField(
                            label=u'División',
                            queryset=Division.objects.all(),
                            required=False
                            ),
            'department': DepartmentChainedSelectWidget(),
            'theory_hours': Select(choices=zip([""]+hours(), ["--"]+hours())),
            'practice_hours': Select(choices=zip([""]+hours(), ["--"]+hours())),
            'laboratory_hours': Select(choices=zip([""]+hours(), ["--"]+hours())),
            'credits': Select(choices=zip([""]+credits(), ["--"]+credits())),
            'validity_date_d': Select(choices=zip([""]+days(), ["--"]+days())),
            'requirements': Textarea(attrs={'class':'materialize-textarea'}),
            'objectives': Textarea(attrs={'class':'materialize-textarea'}),
            'synoptic_content': Textarea(attrs={'class':'materialize-textarea'}),
            'methodological_strategies': Textarea(attrs={'class':'materialize-textarea'}),
            'evaluation_strategies': Textarea(attrs={'class':'materialize-textarea'}),
            'specific_objectives' : Textarea(attrs={'class':'materialize-textarea'}),
            # commit this line when makemigrations and migrate first time
            'coordination': SelectMultipleMaterialize(choices=Coordination.objects.all()),
        }

# Sigpae Search

class SigpaeSearchForm(forms.Form):
    def years():
        return [i for i in range(date.today().year + settings.FUTURE_YEARS, 1968, -1)]
    code = forms.CharField(
        label=u'Código de Materia',
        required=True, 
        max_length=6
        )
    year = forms.ChoiceField(
        label=u'Año', 
        choices=zip([""]+years(), ["------"]+years()),
        required=False
        )
    trimester = forms.ChoiceField(
        label=u'Trimestre', 
        choices=Programa.TRIMESTRE,
        required=False, 
        widget=SelectMaterialize(choices=Programa.TRIMESTRE)
        )

# Reports on SIGPAE
class SigpaeReportForm(forms.Form):
    REPORT = (
        ('Transcripciones', 'Transcripciones'),
        ('Programas', 'Programas'),
        ('Transcripciones y Programas', 'Transcripciones y Programas'),
    )
    code = forms.ModelChoiceField(
        label=u'Código de Dependencia',
        required=True,
        queryset=Code.objects.all(),
        to_field_name="code",
        )
    report_type = forms.ChoiceField(
        label=u'Tipo de reporte',
        choices=REPORT,
        required=True,
    )


# Reports on references
class RefReportForm(forms.Form):
    def years():
        return [i for i in range(date.today().year + settings.FUTURE_YEARS, 1968, -1)]
    code = forms.ModelChoiceField(
        label=u'Código de Dependencia',
        required=False,
        queryset=Code.objects.all(),
        to_field_name="code",
        empty_label=u'Todos',
        )
    year = forms.ChoiceField(
        label=u'Año', 
        choices=zip([""]+years(), ["------"]+years()),
        required=True
        )
    trimester = forms.ChoiceField(
        label=u'Trimestre', 
        choices=Programa.TRIMESTRE,
        required=True, 
        widget=SelectMaterialize(choices=Programa.TRIMESTRE)
        )


# AdditionalField

class AdditionalFieldForm(forms.Form):
    pk = forms.IntegerField(widget=HiddenInput(),
        required=False,)

    name = forms.ModelChoiceField(
        label=u'Nombre', 
        # commit this line when makemigrations and migrate first time
        queryset=AdditionalName.objects.all(),
        required=False,
        )

    new_name = forms.CharField(
        label=u'Nuevo Nombre',
        max_length=30,
        required=False, 
        )

    description = forms.CharField(
        label=u'Contenido',
        required=False, 
        widget=Textarea(attrs={'class':'materialize-textarea'})
        )


class ReferenceForm(forms.ModelForm):
    
    class Meta:
        model = Reference
        exclude = ('author',)
        widgets = {
            'title' : Textarea(attrs={'class':'materialize-textarea'}),
        }

class ProgramReferenceForm(forms.Form):
    reference = forms.ModelChoiceField(
        label=u'Referencia',
        required=False,
        queryset=Reference.objects.all(),
        )