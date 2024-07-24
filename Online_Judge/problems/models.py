from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    constraints = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField(null=True,blank=True)
    output_data = models.TextField(null=True, blank=True)
    hidden = models.BooleanField(default=True)  # Assuming all test cases are hidden

    def __str__(self):
        return f"TestCase for {self.problem.title}"

class CodeSubmission(models.Model):
    language = models.CharField(max_length=100)
    code = models.TextField()
    input_data = models.TextField(null=True,blank=True)
    output_data = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    #result = models.TextField(blank=True, null=True)