import nose.tools as nt

from django.test import TestCase

from nose.tools.nontrivial import raises
import authentication.models as models


# Create your tests here.
class TestSuperUser(TestCase):

    def setUpTestData(self):
        self.user = models.StdUser.objects.create_superuser(email="admin@examole.com", password="Admin123")

    def test_is_staff(self):
        nt.assert_equal(self.user.is_staff, True)

    def test_is_active(self):
        nt.assert_equal(self.user.is_active, True)

    def test_is_superuser(self):
        nt.assert_equal(self.user.is_superuser, True)


class TestStdUser(TestCase):

    def setUpTestData(self):
        self.user = models.StdUser.objects.create_user(email="test@example.com", password="password123")
        self.user.first_name = "Dmitry"
        self.user.last_name = "Pertov"
        self.user.patronymic = "Ivanovich"
        self.user.bio = "TestBio"

    def test_is_active(self):
        nt.assert_equal(self.user.is_active, False)

    def test_email(self):
        nt.assert_equal(self.user.email, 'test@example.com')

    def test_first_name(self):
        nt.assert_equal(self.user.first_name, 'Dmitry')

    def test_last_name(self):
        nt.assert_equal(self.user.last_name, 'Pertov')

    def test_patronymic(self):
        nt.assert_equal(self.user.patronymic, 'Ivanovich')

    def test_bio(self):
        nt.assert_equal(self.user.bio, 'TestBio')

    def test_get_short_name(self):
        short_name = self.user.get_short_name()
        nt.assert_equal(short_name, 'Dmitry')

    def test_get_full_name(self):
        full_name = self.user.get_full_name()
        nt.assert_equal(full_name, 'Dmitry Pertov Ivanovich')


class TestTeacher(TestCase):

    def setUpTestData(self):
        self.user = models.StdUser.objects.create_teacher(email="teacher@example.com", first_name='Andryi', last_name='Kotsuba', password="password123")

    def test_str_method(self):
        nt.assert_equal(str(self.user), self.user.email)

    def test_is_teacher(self):
        nt.assert_equal(self.user.is_teacher, True)


class TestStudent(TestCase):
    def setUpTestData(self):
        self.user = models.StdUser.objects.create_student(email="student@example.com", first_name='Mykola', last_name='Danyliuk', password="password123")

    def test_str_method(self):
        nt.assert_equal(str(self.user), self.user.email)

    def test_is_student(self):
        nt.assert_equal(self.user.is_student, True)