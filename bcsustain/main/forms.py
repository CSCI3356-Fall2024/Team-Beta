from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from django import forms
from .models import Profile
from .models import Campaign



class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_supervisor']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['school', 'graduation_year', 'major1', 'major2', 'profile_picture']

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'start_date', 'end_date', 'location', 'description', 'points', 'delivery_method', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }