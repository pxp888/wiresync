from django.db import models

# Create your models here.
class nwork(models.Model):
    name = models.CharField(max_length=200, unique=True)
    khash = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class peer(models.Model):
    nwork = models.ForeignKey(nwork, on_delete=models.CASCADE, related_name='peers')
    nickname = models.CharField(max_length=200)
    pubkey = models.CharField(max_length=200)
    lanip = models.CharField(max_length=200)
    wanip = models.CharField(max_length=200)
    wgip = models.CharField(max_length=200)
    wgport = models.CharField(max_length=200)

    def __str__(self):
        return self.nickname


