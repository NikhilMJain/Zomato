from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from zomato_search.users.models import User


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.IntegerField()
    text = models.CharField(max_length=2000)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
