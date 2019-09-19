import nose.tools as nt

from django.test import TestCase
from django.core.files import File

from nose.tools.nontrivial import raises
import authentication.models as models


# Create your tests here.
class TestSuperUser(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user = models.StdUser.objects.create_superuser(email="admin@examole.com", password="Admin123")

    def test_is_staff(self):
        nt.assert_equal(self.user.is_staff, True)

    def test_is_active(self):
        nt.assert_equal(self.user.is_active, True)

    def test_is_superuser(self):
        nt.assert_equal(self.user.is_superuser, True)


class TestStdUser(TestCase):
    
    @classmethod
    def setUpTestData(self):
        self.user = models.StdUser.objects.create_user(email="test@example.com", password="Password123")
        self.user.first_name = "Dmitry"
        self.user.last_name = "Pertov"
        self.user.patronymic = "Ivanovich"
        self.user.bio = "TestBio"

    @raises(ValueError)
    def test_without_email(self):
        self.user = models.StdUser.objects.create_user(None, password="password123!");

    def test_hidden_create_user(self):
        self.user = models.StdUser.objects._create_user(
                email="auswahlen.a@gmail.com",
                password="LNTU1233!",)
    
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

    def test_recovery_password(self):
        self.user.send_recovery_password(email='auswahlen.a@gmail.com')

    def test_send_mail(self):
        self.user.send_mail(email='auswahlen.a@gmail.com')

    def test_verify_email(self):
        self.user = models.StdUser.objects.create_user(
            email='auswahlen.a@gmail.com',
            password='Dmytro123!')
        self.user.verify_email(
            code='YXVzd2FobGVuLmFAZ21haWwuY29tOjFpQXZ5Rjp4Tjh2X0MyanlFb2NTeFNXOWwyR2RWeUNubHM') 
    
    def test_verify_email_bad_code(self):
        self.user = models.StdUser.objects.create_user(
            email='auswahlen.a@gmail.com',
            password='Dmytro123!')
        self.user.verify_email(
            code='YXVzd2FobGVuLmF2Z21haWwuY29tOjFpQXZ5Rjp4Tjh2X0MyanlFb2NTeFNXOWwyR2RWeUNubHM') 

    def test_verify_password(self):
        self.user = models.StdUser.objects.create_user(
            email='auswahlen.a@gmail.com',
            password='Dmytro123!')
        self.user.verify_password(
            code='YXVzd2FobGVuLmFAZ21haWwuY29tOjFpQXc1bTpUay1fbTZFdkJxQW9aaFkyRXpKNTF2cll4OGs',
            password='Sanya123!')
   
    def test_get_avatar(self):
        self.user = models.StdUser.objects.create_user(
            email='auswahlen.a@gmail.com',
            password='Leonid123!')

        path = '/opt/docker_polls_group/api/media_files/static/media/photo_2019-04-28_19-50-23_NoXlQnG.jpg'
        self.user.avatar = File(open(path, "rb"))
        self.user.save()
        path = self.user.avatar.path

        nt.assert_equal(self.user.get_avatar(), path)

    @raises(ValueError)
    def test_get_avatar_none(self):
        self.user.get_avatar()

    def test_verify_password_bad_code(self):
        self.user = models.StdUser.objects.create_user(
            email='auswahlen.a@gmail.com',
            password='Dmytro123!')
        self.user.verify_password(
            code='YXCzd2FobGVuLmFAZ21haWwuY29tOjFpQXc1bTpUay1fbTZFdkJxQW9aaFkyRXpKNTF2cll4OGs',
            password='Sanya123!')


class TestTeacher(TestCase):

    @classmethod
    def setUpTestData(self):
        self.faculty = models.Faculty.objects.create(name="FKNIT")
        self.teacher = models.StdUser.objects.create_teacher(
                email="TestTeacher@gmail.com",
                faculty=self.faculty,
                password="TestTeacher123!")

    def test_str(self): 
        nt.assert_equal('TestTeacher@gmail.com', str(self.teacher))
    
    @raises(ValueError)
    def test_without_model(self):
        self.teacher = models.StdUser.objects.create_teacher(
                email="Teaher@gmail.com",
                faculty="FOF",
                password="TestTeacher124!")

    @raises(ValueError)                                                               
    def test_without_email(self):                                                     
        self.user = models.StdUser.objects.create_teacher(
                email=None, 
                faculty=self.faculty,
                password="password123!");


class TestStudent(TestCase):

    @classmethod
    def setUpTestData(self):
        self.profession = models.Profession.objects.create(name="Cybersecurity")            
        self.faculty = models.Faculty.objects.create(name="FKNIT")                          
        self.teacher = models.StdUser.objects.create_student(                          
            email="TestStudent@gmail.com",
            password="TestStudent123!",
            faculty=self.faculty,
            profession=self.profession)   

    def test_str(self):                                            
        nt.assert_equal('TestStudent@gmail.com', str(self.teacher))

    @raises(ValueError)
    def test_without_model(self):                            
        self.teacher = models.StdUser.objects.create_student(
            email="Teaher@gmail.com",                    
            faculty="FOF",    
            profession="Math",
            password="TestTeacher124!")      

    @raises(ValueError)                                                               
    def test_without_email(self):                                                     
        self.user = models.StdUser.objects.create_student(
                email=None, 
                profession=self.profession,
                faculty=self.faculty,
                password="password123!");

class TestMail(TestCase):

    @classmethod
    def setUpTestData(self):
        self.mail = models.Mail.objects.create(
                email="auswahlen.a@gmail.com",
                subject="Theme",
                body="Test body",
        )

    def test_mail(self):
        self.mail.send_mail(self.mail.email, self.mail.subject, self.mail.body)
