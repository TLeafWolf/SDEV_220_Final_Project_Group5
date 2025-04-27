from django.db import models

class Supply(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    location = models.CharField(max_length=255)
    reorder_point = models.PositiveIntegerField(default=5)
    
    def is_low_stock(self):
        return self.quantity <= self.reorder_point

    def __str__(self):
        formatted_price = f"{self.price:.2f}"
        return f"{self.name} (${formatted_price})"

