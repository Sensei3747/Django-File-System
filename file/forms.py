from django import forms
from .models import UserProfile
import re

class UserProfileForm(forms.ModelForm):
    profile_photo_file = forms.ImageField(required= True, label='Profile Photo')

    class Meta:
        model = UserProfile
        fields = ['fname', 'lname', 'age', 'profile_photo_file']

    def clean_profile_photo_file(self):
        photo = self.cleaned_data.get('profile_photo_file')
        if photo:
            if photo.size > 1 * 1024 * 1024:
                raise forms.ValidationError("File size exceeds 1 MB")
        return photo 