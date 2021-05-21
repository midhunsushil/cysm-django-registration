from django.db import models

# Create your models here.

class UserTestScore(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()

    def __str__(self):
        return str(self.name)
