from django.db import models
from table.models import orders
from django.utils import timezone

# Create your models here.
class Bill(models.Model):
    tableNumber = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    orders = models.ManyToManyField(orders)
    created_at = models.DateTimeField(auto_now_add=True)