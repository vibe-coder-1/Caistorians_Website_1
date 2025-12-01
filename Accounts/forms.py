from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import School

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_student_account = forms.BooleanField(required=False, label="I am a student")
    class Meta:
        model = get_user_model()
        #fields = ("username", "email", "school", "is_student_account", "password1", "password2")
        fields = ("username", "email", "is_student_account", "password1", "password2")
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.school = School.objects.get_or_create(name="Caistorians at CGS")[0]
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'graduation_year',
            'name_while_at_school',
            'occupation',
            'bio',
            'linkedin_url',
            'profile_picture',
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'name_while_at_school': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }
