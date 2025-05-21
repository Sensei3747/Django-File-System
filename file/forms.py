from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    profile_photo_file = forms.ImageField(required= True, label='Profile Photo')

    class Meta:
        model = UserProfile
        fields = ['fname', 'lname', 'age', 'profile_photo_file']