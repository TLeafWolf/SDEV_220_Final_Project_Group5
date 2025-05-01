from django.db import models
from django.contrib.auth.models import User  # To link to the user making the change

class Supply(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    location = models.CharField(max_length=255)
    reorder_point = models.PositiveIntegerField(default=5)
    deleted = models.BooleanField(default=False)
    
    def is_low_stock(self):
        return self.quantity <= self.reorder_point

    def __str__(self):
        formatted_price = f"{self.price:.2f}"
        return f"{self.name} (${formatted_price})"


class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Track the user making the change
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)  # The type of action (CREATE, UPDATE, DELETE)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE)  # Link to the supply that was changed
    changes = models.TextField()  # Description of what was changed
    timestamp = models.DateTimeField(auto_now_add=True)  # When the change was made

    def __str__(self):
        return f'{self.action} by {self.user.username} on {self.supply.name} at {self.timestamp}'
