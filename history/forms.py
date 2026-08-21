# events/forms.py
from django import forms
from .models import Event

# events/forms.py
from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "location", "start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert initial datetime to proper HTML5 format
        for field in ["start_time", "end_time"]:
            if self.instance and getattr(self.instance, field):
                self.initial[field] = getattr(self.instance, field).strftime("%Y-%m-%dT%H:%M")


# events/forms.py
from .models import RSVP

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ["status"]

