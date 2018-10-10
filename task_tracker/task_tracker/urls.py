"""task_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import url, include
from task_tracker.views import UserViewSet, GroupViewSet, TaskList, TaskDetail, CommentList, CommentDetail
from rest_framework.urlpatterns import format_suffix_patterns


user_router = routers.DefaultRouter()
user_router.register(r'users', UserViewSet)
user_router.register(r'groups', GroupViewSet)

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(user_router.urls)),
]

urlpatterns += format_suffix_patterns([
    url(r'^api/task/$', TaskList.as_view(), name='tasks'),
    url(r'^api/task/(?P<pk>[0-9]+)/$', TaskDetail.as_view(), name='task-detail'),
    url(r'^api/comment/$', CommentList.as_view(), name='comments'),
    url(r'^api/comment/(?P<pk>[0-9]+)/$', CommentDetail.as_view(), name='comment-detail'),
])
