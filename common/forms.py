from django import forms
from django.core.mail import EmailMessage
from .models import EmailDefaultValues


class SendEmailForm(forms.Form):
    """Send email form. Used to send messages to patients."""

    subject = forms.CharField(max_length=50, required=False)
    recipient = forms.EmailField(required=True)
    message = forms.CharField(required=False, widget=forms.Textarea())
    attachment = forms.FileField(required=False)


class EditEmailDefaultValuesForm(forms.ModelForm):
    class Meta:
        model = EmailDefaultValues
        fields = '__all__'