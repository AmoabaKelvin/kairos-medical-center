from django.shortcuts import redirect, render
from django.core.files.storage import default_storage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from patients.models import Patient
from .forms import SendEmailForm, EditEmailDefaultValuesForm
from .tasks import send_mail
from .models import EmailDefaultValues
from utils.decorators import (
    redirect_to_appropriate_view,
    allow_manager_and_receptionist_only,
)


@login_required(login_url="login")
@redirect_to_appropriate_view
def homepage(request):
    return render(request, "reception/home.html")


@require_http_methods(["GET"])
@allow_manager_and_receptionist_only
def search_for_patient(request):
    """
    Search for users from the database using their names and
    display their info to the template.
    """
    # get the search query from the form box in the html template
    # then filter the results based on the patient's name.
    query = request.GET["user-search"]
    patient = Patient.objects.filter(patients_name__icontains=query)
    context = {"patients": patient}
    return render(request, "common/search.html", context)


def mail(request):
    if request.method == "POST":
        form = SendEmailForm(request.POST, request.FILES)
        if form.is_valid():
            # get the form data and then send them to the celery task.
            subject = form.cleaned_data.get("subject")
            recipient = form.cleaned_data.get("recipient")
            message = form.cleaned_data.get("message")
            attachment = None
            if form.files and form.files["attachment"]:
                attachment = form.files["attachment"]
                attachment = default_storage.save(attachment.name, attachment)

            send_mail.delay(attachment, recipient, subject, message)
            messages.success(request, "Message has been sent successfully.")
            return redirect("send_mail")
    else:
        form = SendEmailForm()

    return render(request, "common/send_mail.html", {"form": form})


def edit_email_defaults(request):
    """
    Handles the editing of the predefined default values of the email subject
    and message body.
    """
    instance_to_use = EmailDefaultValues.objects.first()
    if request.method == "POST":
        form = EditEmailDefaultValuesForm(request.POST, instance=instance_to_use)
        if form.is_valid():
            form.save()
            messages.success(request, "Email Defaults updated successfully")
            return redirect("update_email")
        else:
            form = EditEmailDefaultValuesForm(instance=instance_to_use)
    else:
        form = EditEmailDefaultValuesForm(instance=instance_to_use)
    return render(request, "common/emaildefaults_form.html", {"form": form})
