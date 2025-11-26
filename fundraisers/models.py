from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class Fundraiser(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_raised = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


from community.models import Story
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fundraiser = models.ForeignKey('Fundraiser', on_delete=models.CASCADE, null=True, blank=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)



class UnlockStories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paid = models.BooleanField()
