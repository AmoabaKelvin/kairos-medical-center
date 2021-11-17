from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.conf import settings

from services.models import LabTests

validate_age = MaxValueValidator(150, "Age cannot be greater than 150")


class Patient(models.Model):
    patients_name = models.CharField(max_length=200)
    patients_age = models.PositiveIntegerField(validators=[validate_age])
    patients_contact = models.CharField(max_length=10)
    email_address = models.EmailField(max_length=150)
    tests_to_carry = models.TextField(max_length=500)
    date_added = models.DateField(default=timezone.now)
    receptionist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.patients_name

    def list_of_tests(self) -> list:
        """Returns the tests choices as a list"""
        convert = (
            lambda x: x.replace("[", "")
            .replace("]", "")
            .strip()
            .replace("'", "")
            .split(",")
        )
        return convert(self.tests_to_carry)

    def get_total_test_cost(self):
        tests = self.list_of_tests()
        single_cost = []
        for test in tests:
            print(test)
            single_cost.append(LabTests.objects.get(name__icontains=test.strip()).price)
        return sum(single_cost)


# @receiver(signal=pre_save, sender=Patient)
# def patient_pre_save_receiver(sender, instance, update_fields, *args, **kwargs):
#     update_fields.tests_to_carry.replace('[', '').replace(']', '')
