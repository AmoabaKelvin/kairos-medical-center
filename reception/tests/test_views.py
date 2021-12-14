from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, Group
from django.core.exceptions import PermissionDenied

from customuser.models import CustomUser
from patients.models import Patient
from reception import views
from services.models import LabTests

class TestReceptionViews(TestCase):
    """
    Test the views of the reception application
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user_manager = CustomUser.objects.create(
            username="localhost", email="localhost@test.com", password="123Holyghost"
        )
        self.user_receptionist = CustomUser.objects.create(
            username="reception", email="reception@test.com", password="123Holyghost"
        )
        self.user_manager.groups.add(Group.objects.create(name="manager"))
        self.user_receptionist.groups.add(Group.objects.create(name="reception"))

        # creating a new patient in order to be able to access the patient
        # detail and edit view.
        self.patient = Patient.objects.create(
            patients_name="Kelvin",
            patients_age=43,
            patients_sex="Male",
            patients_contact="0248773454",
            email_address="kelvinamoaba@gmail.com",
            receptionist=self.user_manager,
        )
        self.patient.tests_to_carry.set([LabTests.objects.create(name='FBC', price=30)])

        self.patient_id = self.patient.id

    def test_reception_home_view_for_unallowed(self):
        request = self.factory.get("/reception/")
        request.user = AnonymousUser()
        with self.assertRaises(PermissionDenied):
            views.ReceptionHomeView.as_view()(request)

    def test_reception_home_view_for_manager(self):
        request = self.factory.get("/reception/")
        request.user = self.user_manager
        response = views.ReceptionHomeView.as_view()(request)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("Add New Patient" in str(response.content))

    def test_reception_home_view_for_receptionist(self):
        request = self.factory.get("/reception/")
        request.user = self.user_receptionist
        response = views.ReceptionHomeView.as_view()(request)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("Add New Patient" in str(response.content))

    def test_patient_add_and_edit(self):
        request = self.factory.get("/reception/info/")
        request.user = self.user_manager
        response = views.PatientDetailAndEditView.as_view()(request, self.patient_id)
        self.assertEquals(response.status_code, 200)
