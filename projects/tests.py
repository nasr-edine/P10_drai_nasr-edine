from django.test import TestCase
from django.contrib.auth.models import User

from projects.models import Project


class ProjectTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user
        testuser1 = User.objects.create_user(
            username='testuser1', password='abc123')
        testuser1.save()
        # Create a project
        test_project = Project.objects.create(
            author_user_id=testuser1, title='My project', description='Body content...')
        test_project.save()

    def test_project_content(self):
        project = Project.objects.get(id=1)
        author_user_id = f'{project.author_user_id}'
        title = f'{project.title}'
        description = f'{project.description}'

        self.assertEqual(author_user_id, 'testuser1')
        self.assertEqual(title, 'My project')
        self.assertEqual(description, 'Body content...')
