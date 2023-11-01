from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)


class Stone(models.Model):
    stone_name = models.CharField(max_length=255, unique=True)


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stone = models.ForeignKey(Stone, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
