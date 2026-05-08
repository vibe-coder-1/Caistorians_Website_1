# fundraisers/forms.py
try:
    from django import forms
    from .models import Fundraiser
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

class FundraiserForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ['title', 'description', 'goal_amount']
