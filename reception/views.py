import datetime

from django.views.generic.base import View
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from customuser.models import CustomUser
from patients.models import Patient
from patients.forms import AddPatientForm, EditPatientInfoForm
from .forms import CreateReceptionistForm


def create_receptionist(request):
    """
    Add a new receptionist to the database.
    """
    form = CreateReceptionistForm()
    if request.method == "POST":
        form = CreateReceptionistForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            username = form.cleaned_data.get("username")
            # set the is_worker status to True before saving the user.
            form.instance.is_worker = True
            form.save()
            messages.success(request, f"Account for {username} has been created.")
            return redirect("reception_home")
    context = {"form": form}
    return render(request, "reception/create_receptionist.html", context)


@login_required(login_url="login")
def dashboard(request):
    """
    Get all the patients that were added to the database on a particular
    day and were entered by the currently logged in receptionist.
    """
    if request.user.is_worker:
        today = datetime.date.today().isoformat()
        if request.user.is_superuser:
            patients = Patient.objects.filter(date_added=today)
        else:
            patients = Patient.objects.filter(date_added=today, receptionist=request.user)
        context = {"patients": patients}
        return render(request, "reception/dashboard.html", context)
    raise PermissionDenied


@login_required(login_url="login")
def add_patient(request):
    """
    Add a new patient to the Patient model.
    Only users with is_worker set to True can be able to add the patients.
    """
    form = AddPatientForm()
    if request.method == "POST":
        # if the requested user has a permission of a worker,
        # permit the user to add a patient to the database otherwise return
        # a 403 httpresponse(Permission Denied)
        if request.user.is_worker:
            form = AddPatientForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                # set the receptionist to the currently logged in user
                # before saving.
                form.instance.receptionist = request.user
                form.save()
                messages.success(request, "Success")
                return redirect("reception_home")
        raise PermissionDenied
    return render(request, "reception/home.html", {"form": form})


class PatientDetailAndEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Handle viewing patients details on the detail page and also 
    saving edited patients details.
    """
    def test_func(self):
        # if True is returned, proceed to allow the user to access
        # the views, otherwise raise a 403 response(Permission Denied)
        user = CustomUser.objects.get(email=self.request.user.email)
        if user.is_worker:
            return True
        else:
            return False

    def get(self, request, pk):
        """
        Get a specific patient from the database using the primary key.
        If none is present, raise a 404 error.
        """
        patient = get_object_or_404(Patient, pk=pk)
        # pass a form prefilled with that particular user's info to the
        # context
        form = EditPatientInfoForm(instance=Patient.objects.get(id=pk))
        context = {"patient": patient, "form": form}
        return render(request, "reception/patient_detail_and_edit.html", context)

    def post(self, request, pk):
        """
        Save editted patient info into the database.
        """
        form = EditPatientInfoForm(request.POST, instance=Patient.objects.get(id=pk))
        if form.is_valid():
            form.save()
            messages.success(request, "Patient info updated.")
            return redirect("info", pk)
        return render(request, "reception/patient_detail_and_edit.html")


@require_http_methods(["GET"])
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
    return render(request, "reception/search.html", context)
