from django import forms
from django.core.mail import EmailMessage
from .models import EmailDefaultValues


class SendEmailForm(forms.Form):
    """Send email messages to users."""

    subject = forms.CharField(max_length=50, required=False)
    recipient = forms.EmailField(required=True)
    message = forms.CharField(required=False, widget=forms.Textarea())
    attachment = forms.FileField(required=True)

    def send_email(self):
        subject = self.cleaned_data.get("subject")
        recipient = self.cleaned_data.get("recipient")
        message = self.cleaned_data.get("message")
        file = self.files["attachment"]
        
        # if the subject is not provided, use the default subject.
        # if the message is empty use the default message.
        if not subject:
            subject = EmailDefaultValues.subject
        if not message:
            message = EmailDefaultValues.message_body

        data = b""
        for i in file.chunks(9000000000):
            data += i.strip()

        to_send = EmailMessage(subject=subject, body=message, to=[recipient])
        to_send.attach(file.name, data.strip())

        to_send.send(fail_silently=False)
