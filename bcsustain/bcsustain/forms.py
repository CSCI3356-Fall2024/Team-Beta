from django import forms
from django.contrib.auth import get_user_model

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['is_supervisor']