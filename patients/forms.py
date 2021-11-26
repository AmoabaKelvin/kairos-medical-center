from django import forms
from .models import Patient
from services.models import LabTests


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


class EditPatientInfoForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "patients_name",
            "patients_age",
            "patients_sex",
            "patients_contact",
            "email_address",
        ]
