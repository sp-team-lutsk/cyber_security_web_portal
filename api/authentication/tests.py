import nose.tools as nt

from django.test import TestCase, Client
from django.core.files import File
from django.urls import reverse
from rest_framework.serializers import ValidationError
from django.core.exceptions import ValidationError as django_ValidationError
from django.core.exceptions import ObjectDoesNotExist as DoesNotExist

from nose.tools.nontrivial import raises

import authentication.models as models
import authentication.serializers as a_serializers
import authentication.views as a_views

client = Client()

# Create your tests here.
class TestSuperUser(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user = models.StdUser.objects.create_admin(email="admin@examole.com", password="Admin123")

    def test_is_staff(self):
        nt.assert_equal(self.user.is_staff, True)

    def test_is_active(self):
        nt.assert_equal(self.user.is_active, True)

    def test_is_admin(self):
        nt.assert_equal(self.user.is_admin, True)


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
            code='YXVzd2FobGVuLmFAZ21haWwuY29tOjFpQktWaTpMVjRRQXpNdWwtYlk2Wi1Ock5FU0lENVNRbGM') 
   
    @raises(ValueError)
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
            code='YXVzd2FobGVuLmFAZ21haWwuY29tOjFpQktWaTpMVjRRQXpNdWwtYlk2Wi1Ock5FU0lENVNRbGM',
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

    @raises(ValueError)
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

class TestAPI(TestCase):

    def test_path_user_api(self):
        user = models.StdUser.objects.create_user(email="auswahlen.a@gmail.com", password="teTTTst123!")
        user.is_active = True
        user.save()
        
        client.login(email='auswahlen.a@gmail.com', password='teTTTst123!')

        response = client.patch(reverse('update', kwargs={"pk": user.pk}), {'first_name': 'Leonid'}, content_type='application/json')
        user = models.StdUser.objects.get(email='auswahlen.a@gmail.com')
        nt.assert_equal(response.data, {'Status': 'Update success'})
        nt.assert_equal(user.first_name, "Leonid")


    def test_update_user_api(self):
        user = models.StdUser.objects.create_user(email="auswahlen.a@gmail.com", password="teTTTst123!")
        user.is_active = True
        user.save()

        client.login(email='auswahlen.a@gmail.com', password='teTTTst123!')
        response = client.put(reverse('update', kwargs={"pk": user.pk}), {'first_name': 'Alexandr', 'last_name': 'Shypulin', 'patronymic': '', 'bio': '', 'gender': 'man'}, content_type='application/json')
        nt.assert_equal(response.data, {"Status": "Update success"})
        user = models.StdUser.objects.get(email='auswahlen.a@gmail.com')
        nt.assert_equal(user.first_name, "Alexandr")
        
    def test_send_mail_api(self):
        admin = models.StdUser.objects.create_admin(email="auswahlen.a@gmail.com", password="teTTTst123!") 
        client.login(email='auswahlen.a@gmail.com', password='teTTTst123!')
        response = client.post(reverse('sendmail'), {'email': 'auswahlen.a@gmail.com', 'subject': 'TestSubj', 'body': 'TestBody'})

        nt.assert_equal(response.data, {'Status': 'Mail Send'})

    def test_delete_user(self):
        user = models.StdUser.objects.create_user(email="auswahlen.a@gmail.com", password="teTTTst123!")
        user.is_active = True
        user.save()

        client.login(email='auswahlen.a@gmail.com', password='teTTTst123!')
        response = client.post(reverse('delete'), {'email': 'auswahlen.a@gmail.com', 'password': 'teTTTst123!'})
        user = models.StdUser.objects.get(email='auswahlen.a@gmail.com')
        nt.assert_equal(user.is_active, False)
        nt.assert_equal(response.data, {'Status': 'OK'})

    @raises(DoesNotExist)
    def test_verify_user_serializer(self):
        a_serializers.VerifyUserPassSerializer.post(self, data='fdsfs', code='dsfsdf')

    def test_recovery_error(self):
        user = models.StdUser.objects.create_user(email="auswahlen.a@gmail.com", password="teTTTst123!")
        response = client.post(reverse('recover'), {'email': 'fdsf'})
        nt.assert_equal(response.data, ['This email is not valid'])
    
    def test_active_recovery(self):
        user = models.StdUser.objects.create_user(email="auswahlen.a@gmail.com", password="teTTTst123!")
        user.is_active = True
        user.save()

        response = client.post(reverse('recover'), {'email': 'auswahlen.a@gmail.com'})
        nt.assert_equal(response.data, {'email': 'auswahlen.a@gmail.com'})

    @raises(AssertionError)
    def test_inactive_recovery(self):
        user = models.StdUser.objects.create_user(email="auswahlen.a@gmail.com", password="teTTTst123!")
        response = client.post(reverse('recover'), {'email': 'auswahlen.a@gmail.com'})
        nt.assert_equal(response.data, {'string':'User not active', 'code': 'invalid'})

    def test_verify_password(self):
        user = models.StdUser.objects.create_user(email="auswahlen.a@gmail.com", password="teTTTst123!")
        response = client.post(reverse('completerecover', 
                kwargs={'code': 'YXVzd2FobGVuLmFAZ21haWwuY29tOjFpQktWaTpMVjRRQXpNdWwtYlk2Wi1Ock5FU0lENVNRbGM'}), 
            {'password': 'NewPass!213'},
            kwargs={'code': 'YXVzd2FobGVuLmFAZ21haWwuY29tOjFpQktWaTpMVjRRQXpNdWwtYlk2Wi1Ock5FU0lENVNRbGM'})
        nt.assert_equal(response.data, {"Status": "OK"})
    
    @raises(ValueError)
    def test_activate_user_bad(self):
        user = models.StdUser.objects.create_user(email="auswahlen.a@gmail.com", password="teTTTst123!")
        response = client.get(reverse('verify', kwargs={'code':'YXVzd2FobGVuLmFAZ21haWwuY29tOjFpQXlLUTo1bGtSTGQwY0NqcXZrbTZYVHBScXltZnRpMDA'}))
        nt.assert_equal(response.data, {"Status": "OK"})

    def test_activate_user(self):
        user = models.StdUser.objects.create_user(email="auswahlen.a@gmail.com", password="teTTTst123!")
        response = client.get(reverse('verify', kwargs={'code':'YXVzd2FobGVuLmFAZ21haWwuY29tOjFpQktWaTpMVjRRQXpNdWwtYlk2Wi1Ock5FU0lENVNRbGM'}))
        nt.assert_equal(response.data, {"Status": "OK"})

    @raises(django_ValidationError)
    def test_create_user_bad_pass(self):
        response = client.post(reverse('register'), {"email": "test@example.com", "password": "123324234234"})
        nt.assert_equal(response.data, ["Password must have at least:8 characters, one uppercase/lowercase letter, one symbol, one digit"])


    def test_create_user(self):
        response = client.post(reverse('register'), {"email": "test@example.com", "password": "Test!2334r3d"})
        nt.assert_equal(response.data, {"success": "User 'test@example.com' created successfully"})

    def test_get_inactive(self):
        admin = models.StdUser.objects.create_admin(email="admin@example.com",
                password="Admin123!")
        
        client.login(email="admin@example.com", password="Admin123!")
        response = client.post(reverse('account_inactive')) 
        nt.assert_equal(response.data, {"Account inactive!"}) 
