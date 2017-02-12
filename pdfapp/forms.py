from django import forms


class UploadFileForm(forms.Form):
    docfile = forms.FileField(
        label='Seleccione un archivo'
    )