from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Not provided')
    date_of_birth = models.DateField(null=True, blank=True)
    college = models.CharField(max_length=100, default='Not provided')
    education = models.CharField(max_length=100, default='Not provided')
    city = models.CharField(max_length=100, default='Not provided')
    problems_solved = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
