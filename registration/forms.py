from django import forms
from main.models import Author

class UpdateForm(forms.ModelForm):
    
    class Meta:
        model = Author
        fields = ("first_name", "last_name", "bio", "profile_pic")