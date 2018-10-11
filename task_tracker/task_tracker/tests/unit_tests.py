from django.test import TestCase
from task_tracker.models import Project, Status, Description, Comment, Task


class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name='test_name')

    def test_name_label(self):
        project = Project.objects.get(id=1)
        field_corpus = project._meta.get_field('name').verbose_name
        self.assertEquals(field_corpus, 'name')

    def test_name_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('name').max_length
        self.assertEquals(max_length, 20)

    def test_object_name_is_name(self):
        project = Project.objects.get(id=1)
        expected_object_name = '%s' % project.name
        self.assertEquals(expected_object_name, str(project))


class StatusModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='test_name')

    def test_name_label(self):
        status = Status.objects.get(id=1)
        field_corpus = status._meta.get_field('name').verbose_name
        self.assertEquals(field_corpus, 'name')

    def test_name_max_length(self):
        status = Status.objects.get(id=1)
        max_length = status._meta.get_field('name').max_length
        self.assertEquals(max_length, 20)

    def test_object_name_is_name(self):
        status = Status.objects.get(id=1)
        expected_object_name = '%s' % status.name
        self.assertEquals(expected_object_name, str(status))


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        project = Project.objects.create(name='test_project')
        status = Status.objects.create(name='test_status')
        test_user = User.objects.create_user(username='test_user', password='12345')
        test_user.save()
        Task.objects.create(
            title="test_title",
            project=project,
            status=status,
            assignee=test_user,
            reporter=test_user
        )

    def test_project_label(self):
        task = Task.objects.get(id=1)
        field_corpus = task._meta.get_field('project').verbose_name
        self.assertEquals(field_corpus, 'project')

    def test_status_label(self):
        task = Task.objects.get(id=1)
        field_corpus = task._meta.get_field('status').verbose_name
        self.assertEquals(field_corpus, 'status')

    def test_assignee_label(self):
        task = Task.objects.get(id=1)
        field_corpus = task._meta.get_field('assignee').verbose_name
        self.assertEquals(field_corpus, 'assignee')

    def test_reporter_label(self):
        task = Task.objects.get(id=1)
        field_corpus = task._meta.get_field('reporter').verbose_name
        self.assertEquals(field_corpus, 'reporter')

    def test_title_label(self):
        task = Task.objects.get(id=1)
        field_corpus = task._meta.get_field('title').verbose_name
        self.assertEquals(field_corpus, 'title')

    def test_title_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_title(self):
        task = Task.objects.get(id=1)
        expected_object_name = '%s' % task.id
        self.assertEquals(expected_object_name, str(task))


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        project = Project.objects.create(name='test_project')
        status = Status.objects.create(name='test_status')
        test_user = User.objects.create_user(username='test_user', password='12345')
        test_user.save()
        task = Task.objects.create(
            title="test_title",
            project=project,
            status=status,
            assignee=test_user,
            reporter=test_user
        )
        Comment.objects.create(
            task=task,
            text='test_text',
            author=test_user
        )

    def test_task_label(self):
        comment = Comment.objects.get(id=1)
        field_corpus = comment._meta.get_field('task').verbose_name
        self.assertEquals(field_corpus, 'task')

    def test_text_label(self):
        comment = Comment.objects.get(id=1)
        field_corpus = comment._meta.get_field('text').verbose_name
        self.assertEquals(field_corpus, 'text')

    def test_author_label(self):
        comment = Comment.objects.get(id=1)
        field_corpus = comment._meta.get_field('author').verbose_name
        self.assertEquals(field_corpus, 'author')

    def test_created_label(self):
        comment = Comment.objects.get(id=1)
        field_corpus = comment._meta.get_field('created').verbose_name
        self.assertEquals(field_corpus, 'created')

    def test_object_name_is_corpus(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = '%s' % comment.text
        self.assertEquals(expected_object_name, str(comment))


class DescriptionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        project = Project.objects.create(name='test_project')
        status = Status.objects.create(name='test_status')
        test_user = User.objects.create_user(username='test_user', password='12345')
        test_user.save()
        task = Task.objects.create(
            title="test_title",
            project=project,
            status=status,
            assignee=test_user,
            reporter=test_user
        )
        Description.objects.create(
            task=task,
            text='test_text'
        )

    def test_task_label(self):
        description = Description.objects.get(id=1)
        field_corpus = description._meta.get_field('task').verbose_name
        self.assertEquals(field_corpus, 'task')

    def test_text_label(self):
        description = Description.objects.get(id=1)
        field_corpus = description._meta.get_field('text').verbose_name
        self.assertEquals(field_corpus, 'text')

    def test_created_label(self):
        description = Description.objects.get(id=1)
        field_corpus = description._meta.get_field('created').verbose_name
        self.assertEquals(field_corpus, 'created')

    def test_object_name_is_corpus(self):
        description = Description.objects.get(id=1)
        expected_object_name = '%s' % description.text
        self.assertEquals(expected_object_name, str(description))
