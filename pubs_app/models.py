from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PubsBars(models.Model):
    name = models.CharField(max_length=250)
    map_url = models.URLField()
    open_time = models.TimeField(auto_now=False, auto_now_add=False)
    close_time = models.TimeField(auto_now=False, auto_now_add=False)
    beer_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    outside_tables = models.BooleanField(null=True, blank=True)
    foosball = models.BooleanField(null=True, blank=True)
    overall_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)

    class Meta:
       ordering = ["id"]
    
    def __str__(self):
        return self.name
