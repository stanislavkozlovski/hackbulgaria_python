from django.test import TestCase
from django.core import serializers
from accounts.models import User, Teacher
from course_management_app.models import Course, Lecture


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


class LectureTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='somemanat@abv.bg', password='waytooreal', first_name='Corny')
        Teacher.objects.create(user_email=self.user, courses='placeholder')

        sess = self.client.session
        sess['user'] = serializers.serialize('json', [self.user])
        sess.save()

        self.course_name = 'Java Fundamentals'
        self.client.post('/course/new/', data={'name': self.course_name, 'description': 'Fighting for the glory',
                                               'start_date': '01/02/2013', 'end_date': '02/03/2013'})
        self.course = Course.objects.first()

    def test_create_lecture(self):
        self.client.post('/lecture/new/', data={'name': 'Loops', 'week': '1',
                                                'course': str(self.course.id),
                                                'url': 'http://what.com/?sup=nothing'})
        # Should have created a lecture
        self.assertEqual(Lecture.objects.count(), 1)
        lecture = Lecture.objects.first()
        self.assertEqual(lecture.name, 'Loops')
        self.assertEqual(lecture.week, 1)
        course = Course.objects.first()
        self.assertEqual(lecture.course, course)
        self.assertEqual(course.lecture_set.count(), 1)

    def test_non_teacher_should_not_create_lecture(self):
        self.user = User.objects.create(email='NotATeacher@abv.bg', password='waytooreal', first_name='Corny')

        sess = self.client.session
        sess['user'] = serializers.serialize('json', [self.user])
        sess.save()

        response = self.client.post('/lecture/new/', data={'name': 'Loops', 'week': '1',
                                                'course': str(self.course.id),
                                                'url': 'http://what.com/?sup=nothing'})

        self.assertRedirects(response, '/')
        self.assertEqual(Lecture.objects.count(), 0)
        course = Course.objects.first()
        self.assertEqual(course.lecture_set.count(), 0)
