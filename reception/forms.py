from django import forms
from django.contrib.auth.forms import UserCreationForm
from customuser.models import CustomUser

class CreateReceptionistForm(UserCreationForm):
    """CreateReceptionistForm definition."""

    # this is to create a receptionist for the company.
    # email, first_name, and last_name were overriden to make them required.

    email = forms.EmailField(min_length=10, required=True)
    first_name = forms.CharField(min_length=2, required=True)
    last_name = forms.CharField(min_length=2, required=True)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

