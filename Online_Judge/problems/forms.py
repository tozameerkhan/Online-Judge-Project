# problems/forms.py
from django import forms
from .models import Problem

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'constraints', 'input_format', 'output_format']

class ProblemUpdateForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'constraints', 'input_format', 'output_format']
