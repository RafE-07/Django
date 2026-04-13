from django import forms
from .models import Mediafile

class MediafileForm(forms.ModelForm):
    class Meta:
        model = Mediafile
        fields = ['title', 'file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

def validate_file_size(file):
    max_size = 10 * 1024 * 1024  # 10 MB
    if file.size > max_size:
        raise forms.ValidationError("File size must be under 10 MB.")        