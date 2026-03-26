from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):

    DOMAIN_CHOICES = [
        ('c', 'C Programming'),
        ('py', 'Python'),
        ('java', 'Java'),
        ('web', 'Web Development'),
    ]

    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    question_text = models.TextField()

    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)

    correct_answer = models.IntegerField()  # 1,2,3,4

    def __str__(self):
        return f"{self.domain} - {self.level}"
    
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    score = models.IntegerField()
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"