from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from django.core.exceptions import ValidationError
from .models import User

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirme sua senha", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'gender', 'date_of_birth', 'bio', 'profile_pic']
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            )
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "date_of_birth", "is_active", "is_admin", 'gender', 'date_of_birth', 'update_date']


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ["email", "password", "date_of_birth", "is_active", "is_admin", "gender"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_admin"]}),
        ("Personal Information", {"fields": ["first_name", "last_name", "gender", "date_of_birth", "profile_pic", "bio", "last_login", "update_date"]})
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "date_of_birth", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []



admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
