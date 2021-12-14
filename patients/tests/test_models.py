from django.test import TestCase
from django.urls import reverse

from ..models import Patient
from services.models import LabTests
from customuser.models import CustomUser

class TestPatientModels(TestCase):
    def setUp(self):
        self.user_manager = CustomUser.objects.create(
            username="localhost", email="localhost@test.com", password="123Holyghost"
        )
        self.patient = Patient.objects.create(
            patients_name="Kelvin Amoaba",
            patients_age=43,
            patients_sex="Male",
            patients_contact="0248773454",
            email_address="kelvinamoaba@gmail.com",
            receptionist=self.user_manager,
        )
        self.patient.tests_to_carry.set([LabTests.objects.create(name="FBC", price=30)])

    def test_patient_was_created_successfully(self):
        self.assertIsInstance(self.patient, Patient)
        self.assertIsNotNone(self.patient.id)

    def test_string_representation(self):
        self.assertEquals(str(self.patient), "Kelvin Amoaba")

    def test_absolute_url(self):
        expected_url = reverse("dashboard")
        self.assertEquals(self.patient.get_absolute_url(), expected_url)

    def test_list_representation_of_tests_performed(self):
        returned_data = self.patient.list_of_tests()
        # check that the returned data is of type list
        self.assertIsInstance(returned_data, list)
        self.assertEquals(len(returned_data), 1)
        self.assertEquals(returned_data[0], 'FBC')

    def test_test_performed_price(self):
        price_returned = self.patient.get_price()
        self.assertEquals(price_returned, 30.00)

    def test_days_test_summary(self):
        returned_obj = self.patient.get_todays_test_summary()
        self.assertIsInstance(returned_obj, dict)
        self.assertTrue(len(returned_obj) > 0)
