from django.db import models

# Create your models here.
class nwork(models.Model):
    name = models.CharField(max_length=200, unique=True)
    khash = models.CharField(max_length=100)

    def __str__(self):
        return self.name


