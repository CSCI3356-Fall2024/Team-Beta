from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from .models import Profile
from .models import Campaign
from django.core.exceptions import ValidationError #code inspired from Samary
from datetime import datetime
from .models import Reward

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['google_username', 'google_email', 'graduation_year']

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['school', 'graduation_year', 'major1', 'major2', 'profile_picture']

class ProfileForm(forms.ModelForm):
    current_year = datetime.now().year
    YEAR_CHOICES=[('', 'Select Year')] + [(year,year) for year in range(current_year, current_year +10)]
    graduation_year = forms.ChoiceField(
        choices = YEAR_CHOICES,
        initial = current_year+1,
        widget=forms.Select(attrs={'class':'form-select'})
    )

    profile_picture = forms.ImageField(
        label='Profile Picture',
        widget=forms.ClearableFileInput(attrs={
            'class': 'custom-file-input',
            'id': 'custom-choose-file'
        })
    )
    class Meta:
        model = Profile
        fields = ['google_username', 'google_email', 'school',
                'graduation_year', 'major1', 'major2', 'profile_picture']
        labels = {
            'google_username' : 'Google Username',
            'google_email' : 'Google Email',
            'school': 'School',
            'graduation_year': 'Graduation Year',
            'major1': 'Primary Major',
            'major2': 'Secondary Major (Optional)',
            'profile_picture': 'Profile Picture',
        }


        widgets = {
            'school': forms.TextInput(attrs={'placeholder': 'E.g. Boston College'}),
            'major1': forms.TextInput(attrs={'placeholder': 'E.g. Computer Science'}),
            'major2': forms.TextInput(attrs={'placeholder': 'E.g. Finance'}),
        }

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'points', 'start_date', 'end_date',
        'location', 'description', 'delivery_method', 'add_to_news',
        'is_permanent', 'image']
        labels = {
            'is_permanent': 'Mark as Permanent Campaign',
        }


class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'description', 'points_required', 'available', 'expiration_date']
