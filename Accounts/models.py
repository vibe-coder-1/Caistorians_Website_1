from django.db import models #type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore
from datetime import datetime
from schools.models import School

# Create your models here.
class User(AbstractUser):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="users", null=True, blank=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    name_while_at_school = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_student = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"