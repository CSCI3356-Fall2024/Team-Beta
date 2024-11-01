from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from django import forms
from .models import Profile



# class SupervisorForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ['is_supervisor']  # Include the 'is_supervisor' field


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['school', 'graduation_year', 'major1', 'major2', 'profile_picture']

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_supervisor']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['school', 'graduation_year', 'major1', 'major2', 'profile_picture']