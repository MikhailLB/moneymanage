from django.contrib.auth import get_user_model
from django.db import models

class Budget(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=15, decimal_places=2)
    spent = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} {self.limit} {self.spent}"

    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name