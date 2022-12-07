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

    def __str__(self):
        return self.name

    def show_beer_rating(self):
        rating = []
        for each in range(self.beer_rating):
            rating.append("x")
        return rating

    def show_overall_rating(self):
        rating = []
        for each in range(self.overall_rating):
            rating.append("x")
        return rating