from django import forms
from .models import Photo, Story

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "caption"]

class StoryForm(forms.ModelForm):
    pdf_file = forms.FileField(
        required=False,
        label="Upload a PDF (optional)",
        widget=forms.ClearableFileInput(attrs={'accept': 'application/pdf'})
    )
    text_content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Or type your story here...'})
    )

    class Meta:
        model = Story
        fields = ["title", "pdf_file", "text_content"]