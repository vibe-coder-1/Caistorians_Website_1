from django import forms
from .models import Photo, Story

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "caption"]

# class StoryForm(forms.ModelForm):
#     pdf_file = forms.FileField(
#         required=False,
#         label="Upload a PDF (optional)",
#         widget=forms.ClearableFileInput(attrs={'accept': 'application/pdf'})
#     )
#     text_content = forms.CharField(
#         required=False,
#         widget=forms.Textarea(attrs={'placeholder': 'Or type your story here...'})
#     )

#     class Meta:
#         model = Story
#         fields = ["title", "pdf_file", "text_content"]



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
    price = forms.DecimalField(
        required=False,
        max_digits=8, 
        decimal_places=2,
        label="Price (optional)"
    )
    is_magazine = forms.BooleanField(
        required=False,
        label="Is this a magazine?"
    )
    thumbnail = forms.ImageField(
        required=False,
        label="Thumbnail (optional)"
    )

    class Meta:
        model = Story
        fields = ["title", "text_content", "pdf_file", "price", "is_magazine", "thumbnail"]
