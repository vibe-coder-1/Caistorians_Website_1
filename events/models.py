try:
    from time import timezone
    from django.conf import settings
    from django.db import models
    from django.utils import timezone
    from Accounts.models import School
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

class Event(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="Events",
        default=1
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    def __str__(self):
        return self.title



class RSVP(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="RSVP",
        default=1
    )

    STATUS_CHOICES = [
        ("yes", "Attending"),
        ("maybe", "Maybe"),
        ("no", "Not Attending"),
    ]

    event = models.ForeignKey(Event, related_name="rsvps", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="maybe")
    notes = models.TextField(default="")
    

    class Meta:
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.user.username} → {self.event.title} ({self.status})"
