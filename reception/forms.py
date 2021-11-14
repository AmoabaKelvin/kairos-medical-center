from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from patients.models import Patient


class CreateReceptionistForm(UserCreationForm):
    """CreateReceptionistForm definition."""

    # this is to create a receptionist for the laboratory
    # email, first_name, and last_name were overriden to make them required.

    email = forms.EmailField(min_length=10, required=True)
    first_name = forms.CharField(min_length=2, required=True)
    last_name = forms.CharField(min_length=2, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class AddPatient(forms.ModelForm):
    """Add a patient to the patients list."""

    choices = (
        ("Haemoglobin", "Haemoglobin"),
        ("Malaria", "Malaria"),
        ("Fever", "Fever"),
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
            "tests_to_carry"
        ]
