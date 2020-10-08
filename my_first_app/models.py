from django.db import models

# Create your models here.

class Login(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username

class User_Detail(models.Model):
    username = models.ForeignKey(Login,on_delete=models.PROTECT)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    phone_no = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.email
