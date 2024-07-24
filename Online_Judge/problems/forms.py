# problems/forms.py
from django import forms
from .models import Problem
from .models import CodeSubmission, TestCase

class ProblemForm(forms.ModelForm):
    hidden_input = forms.CharField(widget=forms.Textarea, required=False)
    hidden_output = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Problem
        fields = ['title', 'description', 'constraints', 'input_format', 'output_format', 'hidden_input', 'hidden_output']

class ProblemUpdateForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'constraints', 'input_format', 'output_format']


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['input_data', 'output_data']





LANGUAGE_CHOICES = [
    ("cpp", "C++"),
    #("c", "C"),
    ("py", "Python"),
    
    
]


class CodeSubmissionForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = CodeSubmission
        fields = ["language", "code", "input_data"]
 