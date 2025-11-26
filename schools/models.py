from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="school_logos/", blank=True, null=True)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)

    # Banner
    banner_image = models.ImageField(upload_to="school_banners/", blank=True, null=True)

    def __str__(self):
        return self.name


class HistoricalImage(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="historical_images")
    image = models.ImageField(upload_to="school_historical_images/")
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.school.name} - Historical Image"


class AlumniHighlight(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="alumni_highlights")
    photo = models.ImageField(upload_to="school_alumni_images/")
    name = models.CharField(max_length=255)
    quote = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.school.name})"
