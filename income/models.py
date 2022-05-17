from django.db import models

from authentication.models import User

# Create your models here.
class Income(models.Model):
    SOURCE_OPTIONS = [
        ('SALARY', 'SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('SIDE_HUSTLES', 'SIDE_HUSTLES'),
    ]

    source = models.CharField(choices=SOURCE_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.owner)

    class Meta:
        ordering = ["-date"]