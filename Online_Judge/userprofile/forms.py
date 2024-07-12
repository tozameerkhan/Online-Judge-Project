from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'date_of_birth', 'college', 'education', 'city', 'problems_solved']
