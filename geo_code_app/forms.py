from django import forms
from django.core.validators import FileExtensionValidator


class GeoFileUploadForm(forms.Form):
    '''
        Form class for file upload
    '''
    file = forms.FileField(
            required=True,
            widget=forms.FileInput(
                attrs={
                    'onchange': 'allowed_only_xls (this)',
                    'requried': 'true',
                    'class': "form-control",
                    'accept': ".xls, .xlsx"
                }
            ),
            validators=[FileExtensionValidator(
                allowed_extensions=['xls', 'xlsx'])]
        )
