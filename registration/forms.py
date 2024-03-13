from django import forms
#from main.models import Author
from registration.models import User

class UpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "date_of_birth", "bio", "profile_pic")