from django.db import models

# Create your models here.
class User(models.Model):
    Username=models.CharField(max_length=20)
    Password=models.CharField(max_length=16)
class Task(models.Model):
    Title = models.CharField(max_length=20)
    Description = models.TextField()
    user_id = models.IntegerField()
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, default="Medium")
    due_date = models.CharField(max_length=20, default="", blank=True)