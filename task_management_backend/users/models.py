from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=225 ,unique=True)
  password = models.CharField(max_length=255)
  username = None

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []


class Task(models.Model):
    task_name = models.CharField(max_length=255)
    task_status = models.CharField(max_length=255)
    created_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name