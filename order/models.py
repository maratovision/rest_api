from django.contrib.auth.models import User
from django.db import models
from api.models import Meal
from accounts.models import UserProfile


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    salary = models.IntegerField(default=0)
    schedule = models.CharField(max_length=100)
    order_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.full_name

class Order(models.Model):
    status_choice = (
        ('ready', 'ready'),
        ('in process', 'in process'),
        ('closed', 'closed')
    )
    total_price = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    table = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=status_choice, default='in process')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    worker = models.ForeignKey(EmployeeProfile, on_delete=models.SET_NULL, null=True, blank=True)


class Table(models.Model):
    status_choice = (
        ('Reserved', 'Reserved'),
        ('Empty', 'Empty')
    )
    area = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=status_choice, default='Empty')

    def __str__(self):
        return self.area





class MealToOrder(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='MTO')
    quantity = models.PositiveIntegerField(default=1)
