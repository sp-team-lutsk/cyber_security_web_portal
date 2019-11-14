import nose.tools as nt

from django.test import TestCase

from authentication.models import StdUser

TEST_EMAIL      = "test_email@gmail.com"
TEST_PASSWORD   = "Str0ngp4ss!"
TEST_NAME       = "Alexandr"
TEST_SURNAME    = "Alexandrov"
TEST_PATRONIM   = "Alexandrovich"

class TestStdUser(TestCase):

    ''' This method creates base data for tests '''
    @classmethod
    def setUpTestData(cls):
        cls.user = StdUser.objects.create_user(email=TEST_EMAIL, password=TEST_PASSWORD)
        cls.user.first_name = TEST_NAME
        cls.user.last_name  = TEST_SURNAME
        cls.user.patronymic = TEST_PATRONIM

    ''' Work only when user has is_active status '''
    def test_login(self):
        self.user.is_active = True
        self.user.save()

        login = self.client.login(email=TEST_EMAIL, password=TEST_PASSWORD)
        nt.assert_true(login)

    ''' When user not is_active he cant log in '''
    def test_not_login(self):
        login = self.client.login(email=TEST_EMAIL, password=TEST_PASSWORD)
        nt.assert_false(login)

    ''' Test get_short_name() func '''
    def test_get_short_name(self):
        short_name = self.user.get_short_name()
        nt.assert_equal(short_name, "%s" % (TEST_NAME))

    ''' Test get_full_name() func '''
    def test_get_full_name(self):
        full_name = self.user.get_full_name()
        nt.assert_equal(full_name, "%s %s %s" % (
            TEST_NAME, 
            TEST_SURNAME, 
            TEST_PATRONIM))
