from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator


validate_age = MaxValueValidator(150, "Age cannot be greater than 150")


class Patient(models.Model):
    patients_name = models.CharField(max_length=200)
    patients_age = models.PositiveIntegerField(validators=[validate_age])
    patients_contact = models.IntegerField()
    tests_to_carry = models.TextField(max_length=500)
    date_added = models.DateField(default=timezone.now)
    receptionist = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

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


# @receiver(signal=pre_save, sender=Patient)
# def patient_pre_save_receiver(sender, instance, update_fields, *args, **kwargs):
#     update_fields.tests_to_carry.replace('[', '').replace(']', '')
