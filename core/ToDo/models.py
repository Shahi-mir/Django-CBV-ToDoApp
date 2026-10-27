from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    PRIORITY_CHOICES = [
        ('low','Low'),
        ('medium','Medium'),
        ('high','High')
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(default='')
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium')
    completed = models.BooleanField(default=False,blank=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = "user"