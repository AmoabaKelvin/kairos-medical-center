import os
from celery import shared_task

from django.core.mail import EmailMessage
from django.core.files.storage import default_storage
from django.conf import settings

from .models import EmailDefaultValues


@shared_task
def send_mail(file_name: str, recipient: str, subject: str, message: str):
    """Send an email to the specified recipient

    Args:
        file_name (str): The name of the file to attach to the mail
        recipient (str): The email address of the recipient
        subject (str): Subject of the message.
        message (str): Message body.
    """
    # if the subject or the message are empty, use the default subject and
    # message from the EmailDefaultValues table.
    if not subject:
        subject = EmailDefaultValues.objects.first().subject
    if not message:
        message = EmailDefaultValues.objects.first().message_body
    to_send = EmailMessage(subject=subject, body=message, to=[recipient])
    if file_name:
        # to_send.attach_file(default_storage.path(file_name))
        to_send.attach_file(os.path.join(settings.MEDIA_ROOT, file_name))
    to_send.send(fail_silently=False)
    # After sending the file as an attachment, delete it from the media folder.

    if file_name:
        default_storage.delete(file_name)
