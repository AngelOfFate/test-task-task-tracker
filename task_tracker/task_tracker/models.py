from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    assignee = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='assignees')
    reporter = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reporters')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='authors')

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.text


class Description(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='descriptions')
    text = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.text
