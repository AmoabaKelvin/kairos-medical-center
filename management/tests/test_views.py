from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, Group

from customuser.models import CustomUser
from .. import views


class TestManagementAppViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # create three users. A normal user, a receptionist and a manager
        self.normal_user = CustomUser.objects.create(
            username="normaluser",
            email="normaluser@testing.com",
            password="somerandompassword123",
        )
        self.user_manager = CustomUser.objects.create(
            username="usermanager",
            email="usermanager@testing.com",
            password="somerandompassword123",
        )
        self.user_receptionist = CustomUser.objects.create(
            username="userreceptionist",
            email="userreceptionist@testing.com",
            password="somerandompassword123",
        )
        # set the group of the manager and the receptionist
        manager_group = Group.objects.create(name="manager")
        reception_group = Group.objects.create(name="reception")

        # add the groups for the manager and receptionist
        self.user_manager.groups.add(manager_group)
        self.user_receptionist.groups.add(reception_group)

    def unauthenticated_user_request(self, view_function, url):
        '''
        This method will be called by all tests that need to use an Anonymous 
        user to make a request to a particular view.
        
        Args:
            view_function(function): The function to be testing
            url(str): The url mapping to the view to be tested
        '''
        request = self.factory.get(url)
        request.user = AnonymousUser()
        response = view_function(request)
        # since all anonymous users are unauthenticated, they should all be 
        # directed to the login page since all the views require a user to be
        # authenticated before accessing.
        # hence an expected response code of 302(response code for redirect)
        # is expected. 
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_user_cannot_access_management_homepage(self):
        self.unauthenticated_user_request(views.homepage, '/management/')

    def test_an_authenticated_but_not_allowed_user_cannot_access_management(self):
        request = self.factory.get("/management/")
        request.user = self.normal_user
        with self.assertRaises(PermissionDenied):
            views.homepage(request)

    def test_an_authenticated_and_allowed_user_can_access_management_homepage(self):
        request = self.factory.get("/management/")
        request.user = self.user_manager
        response = views.homepage(request)
        self.assertEqual(response.status_code, 200)

    def test_an_authenticated_user_cannot_access_days_summary(self):
        self.unauthenticated_user_request(views.days_summary, '/management/summary/')

    def test_authenticated_but_not_allowed_user_cannot_access_days_summary(self):
        request = self.factory.get("/management/summary/")
        request.user = self.normal_user
        with self.assertRaises(PermissionDenied):
            views.days_summary(request)

    def test_usermanager_can_access_days_summary_successfully(self):
        request = self.factory.get("/management/summary/")
        request.user = self.user_manager
        response = views.days_summary(request)
        self.assertEqual(response.status_code, 200)

    def test_receptionist_can_access_days_summary(self):
        request = self.factory.get("/management/summary/")
        request.user = self.user_receptionist
        response = views.days_summary(request)
        self.assertEqual(response.status_code, 200)

    def test_get_current_workers_for_unauthenticated_will_not_be_successful(self):
        self.unauthenticated_user_request(views.get_current_workers, '/management/workers/')

    def test_get_current_workers_for_authenticated_but_not_allowed_will_not_work(self):
        request = self.factory.get("/management/workers/")
        request.user = self.user_receptionist
        # make the request with the user with the receptionist first
        # and then make the same request with the normal user.
        # In both cases permission denied ought to be raised.
        with self.assertRaises(PermissionDenied):
            views.get_current_workers(request)

        request.user = self.normal_user
        with self.assertRaises(PermissionDenied):
            views.get_current_workers(request)

    def test_get_current_workers_for_authenticated_and_allowed(self):
        request = self.factory.get("/management/workers/")
        request.user = self.user_manager
        response = views.get_current_workers(request)
        # must produce a 200 response code.
        self.assertEqual(response.status_code, 200)

