try:
    from django.db import models
    from django.conf import settings
    from Accounts.models import User
    from events.models import Event
    from community.models import Photo, Story
    from Accounts.models import School
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")
    print("\n Or required models not found.")
class AdminLog(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="AdminLog",
        default=1
    )
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.username} — {self.action[:50]}"

# Optional: Report model for flagged content
class Report(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="Report",
        default=1
    )
    REPORT_CHOICES = [
        ('photo', 'Photo'),
        ('story', 'Story'),
        ('event', 'Event'),
        ('user', 'User'),
    ]
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, choices=REPORT_CHOICES)
    content_id = models.PositiveIntegerField()
    reason = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reporter.username} flagged {self.content_type} #{self.content_id}"
