from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from task_tracker.models import Project, Status, Description, Comment, Task
from django.contrib.auth.models import User
import json


class TaskCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='test_user_1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='test_user_2', password='12345')
        test_user2.save()

        Project.objects.create(name='IT')
        Project.objects.create(name='TEST')
        Status.objects.create(name='NEW')
        Status.objects.create(name='DONE')

    def test_create_task__without_login(self):
        url = reverse('tasks')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_task__with_login__without_description(self):
        login = self.client.login(username='test_user_1', password='12345')
        data = {
            "title": "1",
            "project": "IT",
            "status": "NEW",
            "assignee": "test_user_1",
            "reporter": "test_user_1",
            "descriptions": []
        }
        response = self.client.post('/api/task/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

        task = Task.objects.get()
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, '1')
        self.assertEqual(task.project.name, 'IT')
        self.assertEqual(task.status.name, 'NEW')
        self.assertEqual(task.assignee.username, 'test_user_1')
        self.assertEqual(task.reporter.username, 'test_user_1')
        self.assertEqual(len(Description.objects.filter(task_id=1)), 0)

    def test_create_task__with_login__with_one_description(self):
        login = self.client.login(username='test_user_1', password='12345')
        data = {
            "title": "2",
            "project": "IT",
            "status": "NEW",
            "assignee": "test_user_1",
            "reporter": "test_user_1",
            "descriptions": [
                "description #1"
            ]
        }
        response = self.client.post('/api/task/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task = Task.objects.get()
        self.assertEqual(task.title, '2')
        self.assertEqual(task.project.name, 'IT')
        self.assertEqual(task.status.name, 'NEW')
        self.assertEqual(task.assignee.username, 'test_user_1')
        self.assertEqual(task.reporter.username, 'test_user_1')
        desc = Description.objects.get()
        self.assertEqual(desc.text, "description #1")

    def test_create_task__with_login__with_descriptions(self):
        login = self.client.login(username='test_user_1', password='12345')
        data = {
            "title": "3",
            "project": "IT",
            "status": "NEW",
            "assignee": "test_user_1",
            "reporter": "test_user_1",
            "descriptions": [
                "description #1", "description #2"
            ]
        }
        response = self.client.post('/api/task/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task = Task.objects.get()
        self.assertEqual(task.title, '3')
        self.assertEqual(task.project.name, 'IT')
        self.assertEqual(task.status.name, 'NEW')
        self.assertEqual(task.assignee.username, 'test_user_1')
        self.assertEqual(task.reporter.username, 'test_user_1')
        for desc in Description.objects.filter(task=task):
            self.assertTrue(desc.text in ["description #1", "description #2"])

    def test_create_task__with_login__with_wrong_params(self):
        login = self.client.login(username='test_user_1', password='12345')
        data = {
            "title": "4",
            "project": "HAHAHA",
            "status": "HAHAHA",
            "assignee": "HAHAHA",
            "reporter": "HAHAHA",
            "descriptions": [123, "description #2"]
        }

        response = self.client.post('/api/task/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data['project'], ["Project HAHAHA not fount"])
        self.assertEqual(response.data['status'], ["Status HAHAHA not fount"])
        self.assertEqual(response.data['assignee'], ["User HAHAHA not fount"])
        self.assertEqual(response.data['reporter'], ["User HAHAHA not fount"])
        self.assertEqual(response.data['descriptions'], ["123: description must be a string or empty"])

    def test_create_task__with_login__with_null_params(self):
        login = self.client.login(username='test_user_1', password='12345')
        data = {
            "title": None,
            "project": None,
            "status": None,
            "assignee": None,
            "reporter": None,
            "descriptions": None
        }

        response = self.client.post('/api/task/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(str(response.data['title'][0]), "This field may not be null.")
        self.assertEqual(response.data['project'], ["This field may not be null."])
        self.assertEqual(response.data['status'], ["This field may not be null."])
        self.assertEqual(response.data['assignee'], ["This field may not be null."])
        self.assertEqual(response.data['reporter'], ["This field may not be null."])
        self.assertEqual(response.data['descriptions'], ["This field may not be null."])


class TaskUpdateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='test_user_1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='test_user_2', password='12345')
        test_user2.save()

        project1 = Project.objects.create(name='IT')
        project2 = Project.objects.create(name='TEST')
        status1 = Status.objects.create(name='NEW')
        status2 = Status.objects.create(name='DONE')

        task = Task.objects.create(
            title="TASK",
            project=project1,
            status=status1,
            assignee=test_user1,
            reporter=test_user2
        )
        description1 = Description.objects.create(task=task, text="description #1")
        description2 = Description.objects.create(task=task, text="description #2")

    def test_update_task__without_login(self):
        url = reverse('task-detail', args=(1,))
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_task__error_params(self):
        login = self.client.login(username='test_user_1', password='12345')
        task_before = Task.objects.get()
        url = reverse('task-detail', args=(1,))
        data = {
            "title": "HAHA",
            "project": "HAHA",
            "reporter": "HAHA",
            "descriptions": ["test"],
        }
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data['project'], ["Project HAHA not fount"])
        self.assertEqual(response.data['reporter'], ["User HAHA not fount"])

    def test_update_task__not_change_other_params(self):
        login = self.client.login(username='test_user_1', password='12345')
        task_before = Task.objects.get()
        url = reverse('task-detail', args=(1,))
        data = {
            "title": "HAHA",
            "project": "IT",
            "reporter": "test_user_1",
            "descriptions": ["test"],
        }
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task_after = Task.objects.get()
        self.assertEqual(task_before, task_after)

    def test_update_task__new_status(self):
        login = self.client.login(username='test_user_1', password='12345')
        task_before = Task.objects.get()
        url = reverse('task-detail', args=(1,))
        data = {
            "status": "DONE"
        }
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get()
        self.assertEqual(task.title, 'TASK')
        self.assertEqual(task.status.name, 'DONE')
        self.assertEqual(task.assignee.username, 'test_user_1')
        self.assertTrue(task_before.updated < task.updated)

    def test_update_task__new_assignee(self):
        login = self.client.login(username='test_user_1', password='12345')
        task_before = Task.objects.get()
        url = reverse('task-detail', args=(1,))
        data = {
            "assignee": "test_user_2"
        }
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get()
        self.assertEqual(task.title, 'TASK')
        self.assertEqual(task.status.name, 'NEW')
        self.assertEqual(task.assignee.username, 'test_user_2')
        self.assertTrue(task_before.updated < task.updated)

    def test_update_task__new_status_and_assignee(self):
        login = self.client.login(username='test_user_1', password='12345')
        task_before = Task.objects.get()
        url = reverse('task-detail', args=(1,))
        data = {
            "status": "NEW",
            "assignee": "test_user_1"
        }
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get()
        self.assertEqual(task.title, 'TASK')
        self.assertEqual(task.status.name, 'NEW')
        self.assertEqual(task.assignee.username, 'test_user_1')
        self.assertTrue(task_before.updated < task.updated)


class TaskDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='test_user_1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='test_user_2', password='12345')
        test_user2.save()

        project1 = Project.objects.create(name='IT')
        status1 = Status.objects.create(name='NEW')

        task = Task.objects.create(
            title="TASK",
            project=project1,
            status=status1,
            assignee=test_user1,
            reporter=test_user2
        )
        Description.objects.create(task=task, text="description #1")
        Description.objects.create(task=task, text="description #2")

        Comment.objects.create(task=task, text="Comment #1", author=test_user1)
        Comment.objects.create(task=task, text="Comment #2", author=test_user2)

    def test_delete_task__without_login(self):
        url = reverse('task-detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        login = self.client.login(username='test_user_1', password='12345')
        url = reverse('task-detail', args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
        self.assertEqual(Description.objects.count(), 0)
        self.assertEqual(Comment.objects.count(), 0)


class CommentAddTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='test_user_1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='test_user_2', password='12345')
        test_user2.save()

        project1 = Project.objects.create(name='IT')
        status1 = Status.objects.create(name='NEW')

        task = Task.objects.create(
            title="TASK",
            project=project1,
            status=status1,
            assignee=test_user1,
            reporter=test_user2
        )
        Description.objects.create(task=task, text="description #1")
        Description.objects.create(task=task, text="description #2")

    def test_add_comment__without_login(self):
        url = reverse('comments')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_comment(self):
        login = self.client.login(username='test_user_1', password='12345')
        url = reverse('comments')
        data = {
            'task': 1,
            'author': 'test_user_2',
            'text': 'Comment text #1',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.get()
        self.assertEqual(comment.author.username, 'test_user_2')
        self.assertEqual(comment.text, 'Comment text #1')
        self.assertTrue(comment.created)

    def test_add_one_more_comment(self):
        login = self.client.login(username='test_user_1', password='12345')
        url = reverse('comments')
        data = {
            'task': 1,
            'author': 'test_user_1',
            'text': 'Comment text #2',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment2 = Comment.objects.get()
        self.assertEqual(comment2.author.username, 'test_user_1')
        self.assertEqual(comment2.text, 'Comment text #2')
        self.assertTrue(comment2.created)

    def test_comments_count(self):
        login = self.client.login(username='test_user_1', password='12345')
        url = reverse('comments')
        data1 = {
            'task': 1,
            'author': 'test_user_2',
            'text': 'Comment text #1',
        }
        data2 = {
            'task': 1,
            'author': 'test_user_1',
            'text': 'Comment text #2',
        }
        self.client.post(url, data=data1)
        self.client.post(url, data=data2)

        task = Task.objects.get()
        comments = task.comments.all()
        self.assertEqual(len(comments), 2)
        self.assertTrue(comments[0].created > comments[1].created)


class TaskListViewTest(TestCase):  # with filters
    @classmethod
    def setUpTestData(cls):
        #
        test_user1 = User.objects.create_user(username='test_user_1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='test_user_2', password='12345')
        test_user2.save()

        project1 = Project.objects.create(name='TEST')
        project2 = Project.objects.create(name='IT')
        status1 = Status.objects.create(name='NEW')
        status2 = Status.objects.create(name='DONE')

        # Create 5 tasks in project TEST and IT
        number_of_tasks = 5
        for project in [project1, project2]:
            for task_num in range(number_of_tasks):
                task = Task.objects.create(
                    title='task #{}'.format(task_num),
                    project=project,
                    status=status1,
                    assignee=User.objects.get(username='test_user_1'),
                    reporter=User.objects.get(username='test_user_2')
                )
                Description.objects.create(task=task, text="description#1 for task{}".format(task_num))
                Description.objects.create(task=task, text="description#2 for task{}".format(task_num))

                Comment.objects.create(task=task, text="Comment#1 for task{}".format(task_num), author=test_user1)
                Comment.objects.create(task=task, text="Comment#2 for task{}".format(task_num), author=test_user2)

    def test_task_list__without_login(self):
        url = reverse('tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_task_list__without_filter(self):
        login = self.client.login(username='test_user_1', password='12345')
        url = reverse('tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_task_list__with_search(self):
        login = self.client.login(username='test_user_1', password='12345')
        response = self.client.get('/api/task/?search=task4')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_task_list__with_filter_by_title(self):
        login = self.client.login(username='test_user_1', password='12345')
        response = self.client.get('/api/task/?title=task %233')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_task_list__with_filter_by_project(self):
        login = self.client.login(username='test_user_1', password='12345')
        response = self.client.get('/api/task/?project=IT')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_task_list__with_filter_by_status(self):
        login = self.client.login(username='test_user_1', password='12345')
        response = self.client.get('/api/task/?status=NEW')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_task_list__with_filter_by_assignee(self):
        login = self.client.login(username='test_user_1', password='12345')
        response = self.client.get('/api/task/?assignee=test_user_1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_task_list__with_filter_by_reporter(self):
        login = self.client.login(username='test_user_1', password='12345')
        response = self.client.get('/api/task/?reporter=test_user_1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_task_list__with_filter_by_descriptions(self):
        login = self.client.login(username='test_user_1', password='12345')
        response = self.client.get('/api/task/?descriptions=description%231 for task2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class TaskDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='test_user_1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='test_user_2', password='12345')
        test_user2.save()

        project1 = Project.objects.create(name='IT')
        project2 = Project.objects.create(name='TEST')
        status1 = Status.objects.create(name='NEW')

        task1 = Task.objects.create(
            title="TASK #1",
            project=project1,
            status=status1,
            assignee=test_user1,
            reporter=test_user2
        )
        Description.objects.create(task=task1, text="description #1")
        Description.objects.create(task=task1, text="description #2")

        Comment.objects.create(task=task1, text="Comment #1", author=test_user1)
        Comment.objects.create(task=task1, text="Comment #2", author=test_user2)

        task2 = Task.objects.create(
            title="TASK #2",
            project=project2,
            status=status1,
            assignee=test_user1,
            reporter=test_user2
        )
        Description.objects.create(task=task2, text="description #1")
        Description.objects.create(task=task2, text="description #2")

        Comment.objects.create(task=task2, text="Comment #1", author=test_user1)
        Comment.objects.create(task=task2, text="Comment #2", author=test_user2)

    def test_task_detail__without_login(self):
        url = reverse('task-detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_check_task_list(self):
        login = self.client.login(username='test_user_1', password='12345')
        response = self.client.get('/api/task/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['title'], "TASK #1")
        self.assertEqual(response.data[0]['project'], "IT")
        self.assertEqual(response.data[0]['status'], "NEW")
        self.assertEqual(response.data[0]['assignee'], "test_user_1")
        self.assertEqual(response.data[0]['reporter'], "test_user_2")
        self.assertEqual(response.data[0]['descriptions'], ['description #1', 'description #2'])

        self.assertEqual(response.data[1]['id'], 2)
        self.assertEqual(response.data[1]['title'], "TASK #2")
        self.assertEqual(response.data[1]['project'], "TEST")
        self.assertEqual(response.data[1]['status'], "NEW")
        self.assertEqual(response.data[1]['assignee'], "test_user_1")
        self.assertEqual(response.data[1]['reporter'], "test_user_2")
        self.assertEqual(response.data[1]['descriptions'], ['description #1', 'description #2'])

        self.assertTrue(response.data[1]['created'] > response.data[0]['created'])
