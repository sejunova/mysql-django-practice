from django.db import models


class Fitness(models.Model):
    name = models.CharField(max_length=45, unique=True)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=25)

    def __str__(self):
        return self.name