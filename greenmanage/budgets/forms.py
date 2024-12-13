from django import forms
from .models import Budget, Category

class AddLimitForm(forms.ModelForm):
    reminder = forms.CharField(max_length=255)
    class Meta:
        fields = ['limit']

