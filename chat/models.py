from django.db import models
from django.conf import settings
import hashlib

class GroupChatRoom(models.Model):
    cohort_year = models.IntegerField(unique=True)

    def __str__(self):
        return f"Cohort {self.cohort_year}"


class GroupMessage(models.Model):
    room = models.ForeignKey(
        GroupChatRoom, on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=500, blank=True)  # store hex color

    class Meta:
        ordering = ['sent_at']

    def save(self, *args, **kwargs):
        if not self.color:
            self.color = self.generate_color(self.sender.username)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_color(username):
        """
        Generate a consistent blue pastel color for a username.
        Hue fixed around 200° (blue), saturation and lightness vary slightly based on hash.
        """
        import hashlib
        hash_int = int(hashlib.md5(username.encode()).hexdigest()[:6], 16)

        # Fixed hue for blue (~200 degrees)
        hue = 200
        # Vary saturation 50%-80%
        sat = 50 + (hash_int % 31)
        # Vary lightness 70%-85%
        light = 70 + (hash_int % 16)

        return f"hsl({hue}, {sat}%, {light}%)"


    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}"
