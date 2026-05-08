try:
    from django import forms 
    from django.forms import modelformset_factory 
    from .models import School, HistoricalImage, AlumniHighlight
    from Accounts.models import User
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

class SchoolForm(forms.ModelForm):
    staff_username = forms.CharField(max_length=150)
    staff_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = School
        fields = ['name', 'logo', 'description', 'address', 'banner_image', 'staff_username', 'staff_password']

    def save(self, commit=True):
        school = super().save(commit=commit)

        # Create the staff user
        username = self.cleaned_data['staff_username']
        password = self.cleaned_data['staff_password']

        staff_user = User.objects.create_user(
            username=username,
            password=password,
            school=school,
            is_staff_account=True
        )

        return school


# Form for HistoricalImage
class HistoricalImageForm(forms.ModelForm):
    class Meta:
        model = HistoricalImage
        fields = ['image', 'caption']


# Form for AlumniHighlight
class AlumniHighlightForm(forms.ModelForm):
    class Meta:
        model = AlumniHighlight
        fields = ['photo', 'name', 'quote']


# Formsets (extra=1 means at least one blank form will always show)
HistoricalImageFormSet = modelformset_factory(HistoricalImage, form=HistoricalImageForm, extra=3, can_delete=True)
AlumniHighlightFormSet = modelformset_factory(AlumniHighlight, form=AlumniHighlightForm, extra=3, can_delete=True)


try:
    from django import forms
    from django.forms import inlineformset_factory
    from .models import School, HistoricalImage, AlumniHighlight
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

class EditSchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'logo', 'description', 'address', 'banner_image']

# Inline formsets for related images
HistoricalImageFormSet = inlineformset_factory(
    parent_model=School,
    model=HistoricalImage,
    fields=['image', 'caption'],
    extra=1,        # always show at least 1 empty form to add
    can_delete=True # allow deleting
)

AlumniHighlightFormSet = inlineformset_factory(
    parent_model=School,
    model=AlumniHighlight,
    fields=['photo', 'name', 'quote'],
    extra=1,
    can_delete=True
)
