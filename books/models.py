from django.db import models
from django.core.validators import MinValueValidator

class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
