import django_filters.rest_framework
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from task_tracker.serializers import UserSerializer, GroupSerializer, TaskSerializer, CommentSerializer
from task_tracker.models import Task, Comment
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend)
    search_fields = (
        'title',
        'project__name',
        'status__name',
        'assignee__username',
        'reporter__username',
        'descriptions__text'
    )

    def get_queryset(self):
        params_dict = settings.TASK_PARAMS_DICT
        queryset = Task.objects.all()
        queue_dict = {}

        for param in params_dict:
            query_param = self.request.query_params.get(param, None)
            if query_param is not None:
                queue_dict[params_dict[param]] = query_param

        queryset = queryset.filter(**queue_dict)
        return queryset


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
