from django import forms
from .models import Patient
from django_select2.forms import Select2MultipleWidget


class AddPatientForm(forms.ModelForm):
    """Add a patient to the patients list."""

    class Meta:
        model = Patient
        fields = [
            "patients_name",
            "patients_age",
            "patients_sex",
            "patients_contact",
            "email_address",
            "tests_to_carry",
        ]
        widgets = {
            # using select2multiple widget in order to enable searching
            # for entries from the reception ui.
            "tests_to_carry": Select2MultipleWidget()
        }


class EditPatientInfoForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "patients_name",
            "patients_age",
            "patients_sex",
            "patients_contact",
            "email_address",
            "tests_to_carry",
        ]
        widgets = {"tests_to_carry": Select2MultipleWidget()}
