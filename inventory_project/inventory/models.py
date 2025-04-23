from django.db import models

class Supply(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

