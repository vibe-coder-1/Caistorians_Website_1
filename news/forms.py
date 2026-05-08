try:
    from urllib import request
    from django import forms
    from .models import Births_Deaths_and_Marriages
except ImportError as e:
    print(f"\nError: Required modules are not installed. {e}\nPlease ensure Django is installed using: pip install django\n")

class Births_Deaths_and_MarriagesForm(forms.ModelForm):
    class Meta:
        model = Births_Deaths_and_Marriages
        fields = ['title', 'content', 'image', 'publication_date']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }