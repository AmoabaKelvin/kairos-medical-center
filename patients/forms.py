from django import forms
from .models import Patient


class AddPatientForm(forms.ModelForm):
    """Add a patient to the patients list."""

    choices = (
        ("Haemoglobin", "Haemoglobin"),
        ("Malaria", "Malaria"),
        ("Fever", "Fever"),
        ("Ebola", "Ebola"),
    )
    tests_to_carry = forms.MultipleChoiceField(
        choices=choices, widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Patient
        fields = [
            "patients_name",
            "patients_age",
            "patients_contact",
            "email_address",
            "tests_to_carry",
        ]


class EditPatientInfoForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["patients_name", "patients_age", "patients_contact", "email_address"]
