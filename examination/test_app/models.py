from django.db import models
from django.contrib.auth.models import User

class QuestionPaper(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    paper = models.ForeignKey(QuestionPaper, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    marks = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, null=True)
    marks = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.paper.title if self.paper else 'General'} - {self.marks}"
