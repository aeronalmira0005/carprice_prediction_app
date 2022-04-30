from django.db import models


class Prediction(models.Model):

    def __str__(self):
        return self.brand

    mileage = models.IntegerField()
    enginev = models.FloatField()
    brand = models.CharField(max_length=200)
    body = models.CharField(max_length=200)
    engine_type = models.CharField(max_length=200)
    registration = models.BooleanField()
    predicted_price = models.FloatField()
