from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name

class Todo_Task(models.Model):
    project = models.ForeignKey(Project, related_name='todo_tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    reminder = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    votes = models.IntegerField(default=0)
    suggestions = models.TextField(blank=True)


    def __str__(self):
        return self.title


class Suggestion(models.Model):
    todo_task = models.ForeignKey(Todo_Task, related_name='suggestion_list', on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Suggestion by {self.user} on {self.todo_task.title}'

class InviteToProject(models.Model):
    email = models.EmailField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    token = models.CharField(max_length=200, unique=True)
    expire_date = models.DateTimeField(default=timezone.now() + timedelta(days=7))
    is_accepted = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expire_date