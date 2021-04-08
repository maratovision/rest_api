from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    phone = models.IntegerField(default=0)
    street = models.CharField(max_length=10)
    house = models.CharField(max_length=10)
    email = models.EmailField()
    bonuses = models.PositiveIntegerField(default=0, blank=True)
    order_count = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return self.full_name


class Cards(models.Model):
    balance = models.PositiveIntegerField(default=0)
    number = models.IntegerField()
    holder_name = models.CharField(max_length=50)
    date = models.DateField()
    code = models.IntegerField()
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return f"{self.holder_name}, {self.number}"
