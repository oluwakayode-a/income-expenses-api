from django.db import models

from authentication.models import User

# Create your models here.
class Expense(models.Model):
    CATEGORY_OPTIONS = [
        ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
        ('TRAVEL', 'TRAVEL'),
        ('RENT', 'RENT'),
    ]

    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)