from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    status = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(default = 0)

    def __str__(self):
        return self.title