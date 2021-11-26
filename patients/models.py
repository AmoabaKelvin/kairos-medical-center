import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.conf import settings
from django.urls import reverse

from services.models import LabTests

validate_age = MaxValueValidator(150, "Age cannot be greater than 150")


class Patient(models.Model):
    gender_choices = (("Female", "Female"), ("Male", "Male"))
    patients_name = models.CharField(max_length=200)
    patients_age = models.PositiveIntegerField(validators=[validate_age])
    patients_sex = models.CharField(max_length=6, choices=gender_choices)
    patients_contact = models.CharField(max_length=10)
    email_address = models.EmailField(max_length=150, blank=True)
    tests_to_carry = models.ManyToManyField(LabTests)
    date_added = models.DateField(default=timezone.now)
    receptionist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.patients_name

    def list_of_tests(self) -> list:
        """Returns the tests choices as a list"""
        return [x.name for x in self.tests_to_carry.all()]

    def get_price(self):
        """
        Get the total price of the tests that were carried out on a patent.
        """
        return sum([i.price for i in self.tests_to_carry.all()])

    @staticmethod
    def tests_performed_today():
        patients = Patient.objects.filter(date_added=datetime.date.today().isoformat())
        tests = [x.name for c in patients for x in c.tests_to_carry.all()]
        unique_tests = set(tests)
        cost = []
        for i in unique_tests:
            test_occurances = tests.count(i)
            cost.append((test_occurances * LabTests.get_price(i)))
        return len(tests), sum(cost)

    @staticmethod
    def get_todays_test_summary(date_added=None):
        """
        Get the total number of unique tests done and then compute the prices.
        """
        # get the tests that were performed by patients today into a list
        if not date_added:
            date_added = datetime.date.today().isoformat()
        patients = Patient.objects.filter(date_added=date_added)
        if patients:
            tests = [x.name for c in patients for x in c.tests_to_carry.all()]
            # make a set of the items in the test to make them unique
            unique_tests = set(tests)
            # initialize an empty dictionary to store the test, the number of appearance
            # and the price
            patient = {}
            for i in unique_tests:
                # count the number of each test in the unique_tests object
                # and then compute the price, then add it to the empty, dictionary.
                test_occurances = tests.count(i)
                patient[i] = [test_occurances, test_occurances * LabTests.get_price(i)]
            return patient

    def get_absolute_url(self):
        return reverse("dashboard")
