try:
    from django.utils import timezone
    from django.db import models
    from schools.models import School
except ImportError as e:
    print(f"\nError: Required modules are not installed. {e}\nPlease ensure Django is installed using: pip install django\n")

# Create your models here.

class Births_Deaths_and_Marriages(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="bdm_updates", null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="news/articles", null=True, blank=True)

    def __str__(self):
        return self.title