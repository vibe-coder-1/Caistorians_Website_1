try:
    from django import forms
    from .models import Message
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["recipient", "subject", "body"]
