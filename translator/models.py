from django.db import models


# Create your models here.
class Input_text(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.name
