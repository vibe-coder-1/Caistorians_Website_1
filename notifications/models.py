from django.db import models

# Create your models here.
# notifications/models.py
from django.db import models

from django.utils import timezone
from schools.models import School
from django.contrib.auth import get_user_model
User = get_user_model()

class Notification(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.school:
            return f"{self.title} ({self.school.name})"
        return f"{self.title} (Individual)"


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notifications")
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="user_states")
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'notification')
