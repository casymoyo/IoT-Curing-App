from django import forms
from .models import Config

class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = ['stage', 'name', 'lower_limit_value', 'upper_limit_value', 'user']
