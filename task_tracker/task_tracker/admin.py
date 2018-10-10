from django.contrib import admin
from django import forms
from .models import *


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


class DescriptionInline(admin.TabularInline):
    model = Description
    extra = 1


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'task',
        'author',
        'created',
        'text',
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [
        DescriptionInline,
    ]

    list_display = (
        'title',
        'project',
        'status',
        'assignee',
        'reporter',
        'created',
        'updated',
    )
