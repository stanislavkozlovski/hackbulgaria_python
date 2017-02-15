from django.test import TestCase
from django.core import serializers
from accounts.models import User, Teacher
from course_management_app.models import Course


class CourseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='somemanat@abv.bg', password='waytooreal', first_name='Corny')
        sess = self.client.session
        sess['user'] = serializers.serialize('json', [self.user])
        sess.save()

    def test_create_course(self):
        """ Should create a course """
        # We need to be a logged in teacher to post it
        Teacher.objects.create(user_email=self.user, courses='placeholder')

        self.client.post('/course/new/', data={'name': 'Java FUndamentals', 'description': 'Fighting for the glory',
                                               'start_date': '01/02/2013', 'end_date': '02/03/2013'})

        self.assertEqual(Course.objects.count(), 1)
        course = Course.objects.first()
        self.assertEqual(course.name, 'Java FUndamentals')
        self.assertEqual(course.description, 'Fighting for the glory')

    def test_non_teacher_should_not_create_course(self):
        """ Should not create a course """
        # We need to be a logged in teacher to post it
        self.client.post('/course/new/', data={'name': 'Java FUndamentals', 'description': 'Fighting for the glory',
                                               'start_date': '01/02/2013', 'end_date': '02/03/2013'})

        self.assertEqual(Course.objects.count(), 0)

    def test_edit_course(self):
        """ Should edit the course """
        Teacher.objects.create(user_email=self.user, courses='placeholder')
        self.client.post('/course/new/', data={'name': 'Java FUndamentals', 'description': 'Fighting for the glory',
                                               'start_date': '01/02/2013', 'end_date': '02/03/2013'})
        course = Course.objects.first()
        self.client.post(f'/course/edit/{course.name}/', data={'name': 'NewName',
                                                               'description': 'Fighting for the glory',
                                                               'start_date': '01/02/2013', 'end_date': '02/03/2013'})
        course.refresh_from_db()
        self.assertEqual(course.name, 'NewName')

    def test_non_teacher_should_not_edit_course(self):
        # Turn the current User into a teacher
        Teacher.objects.create(user_email=self.user, courses='placeholder')
        # Create the course
        self.client.post('/course/new/', data={'name': 'Java FUndamentals', 'description': 'Fighting for the glory',
                                               'start_date': '01/02/2013', 'end_date': '02/03/2013'})
        # 'log in' as a new user who is not a teacher
        self.user = User.objects.create(email='NEWMAN@abv.bg', password='waytooreal', first_name='Corny')
        sess = self.client.session
        sess['user'] = serializers.serialize('json', [self.user])
        sess.save()

        course = Course.objects.first()

        # Try to edit the course
        self.client.post(f'/course/edit/{course.name}/', data={'name': 'NewName',
                                                               'description': 'Fighting for the glory',
                                                               'start_date': '01/02/2013', 'end_date': '02/03/2013'})

        # Assert it has not changed
        course.refresh_from_db()
        self.assertEqual(course.name, 'Java FUndamentals')
