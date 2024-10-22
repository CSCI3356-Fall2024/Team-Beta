from django import forms
from django.contrib.auth import get_user_model
from .models import Profile



# trying the one below
# class SupervisorForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         #fields = ['is_supervisor']
#         fields = []

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['is_supervisor']  # Include the 'is_supervisor' field

# class SupervisorForm(forms.Form):
#     is_supervisor = forms.ChoiceField(
#         choices=[(True, 'Yes'), (False, 'No')],
#         widget=forms.Select()
#     )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['school', 'graduation_year', 'major1', 'major2', 'profile_picture']