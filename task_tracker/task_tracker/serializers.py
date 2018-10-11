from django.contrib.auth.models import User, Group
from rest_framework import serializers
from task_tracker.models import Project, Status, Description, Comment, Task
from django.core.exceptions import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class StatusField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        try:
            status = Status.objects.get(name=data)
            return status
        except ObjectDoesNotExist:
            raise ValidationError('Status {} not fount'.format(data))


class ProjectField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        try:
            project = Project.objects.get(name=data)
            return project
        except ObjectDoesNotExist:
            raise ValidationError('Project {} not fount'.format(data))


class DescriptionField(serializers.RelatedField):
    def to_representation(self, value):
        return value.text

    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise ValidationError('{}: description must be a string or empty'.format(data))
        else:
            return data


class TaskField(serializers.RelatedField):
    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        try:
            task = Task.objects.get(id=data)
            return task
        except ObjectDoesNotExist:
            raise ValidationError('Task {} not fount'.format(data))
        except ValueError:
            raise ValidationError('{}: task id must be integer'.format(data))


class UserField(serializers.RelatedField):
    def to_representation(self, value):
        return value.username

    def to_internal_value(self, data):
        try:
            user = User.objects.get(username=data)
            return user
        except ObjectDoesNotExist:
            raise ValidationError('User {} not fount'.format(data))


class CommentSerializer(serializers.ModelSerializer):
    author = UserField(queryset=User.objects.all())
    task = TaskField(queryset=Task.objects.all())

    class Meta:
        model = Comment
        fields = ('author', 'created', 'text', 'task')

    def create(self, validated_data):
        comment = super(CommentSerializer, self).create(validated_data)
        validated_data['task'].save()

        return comment


class TaskSerializer(serializers.ModelSerializer):
    descriptions = DescriptionField(queryset=Description.objects.all(), many=True)
    comments = CommentSerializer(read_only=True, many=True)

    project = ProjectField(queryset=Project.objects.all())
    status = StatusField(queryset=Status.objects.all())
    assignee = UserField(queryset=User.objects.all())
    reporter = UserField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'project',
            'status',
            'assignee',
            'reporter',
            'created',
            'updated',
            'descriptions',
            'comments',
        )

    def create(self, validated_data):
        task = Task.objects.create(
            title=validated_data['title'],
            project=validated_data['project'],
            status=validated_data['status'],
            assignee=validated_data['assignee'],
            reporter=validated_data['reporter']
        )

        for desc in validated_data['descriptions']:
            Description.objects.create(task=task, text=desc)

        return task

    def update(self, instance, validated_data):
        status = validated_data.get('status', None)
        assignee = validated_data.get('assignee', None)
        if status:
            instance.status = validated_data['status']
        if assignee:
            instance.assignee = validated_data['assignee']
        if status or assignee:
            instance.save()

        return instance

