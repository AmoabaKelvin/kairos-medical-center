import datetime

from django.views.generic.base import View
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from .forms import CreateReceptionistForm
from patients.models import Patient
from patients.forms import AddPatientForm, EditPatientInfoForm
from .decorators import (
    redirect_to_appropriate_view,
    allow_receptionist_only,
    allow_manager_and_receptionist_only,
)



@login_required(login_url="login")
@redirect_to_appropriate_view
def homepage(request):
    return render(request, "reception/home.html")


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
@allow_manager_and_receptionist_only
def dashboard(request):
    """
    Get all the patients that were added to the database on a particular
    day and were entered by the currently logged in receptionist.
    """
    today = datetime.date.today().isoformat()
    if request.user.is_manager:
        patients = Patient.objects.filter(date_added=today)
    else:
        patients = Patient.objects.filter(date_added=today, receptionist=request.user)
    context = {"patients": patients}
    return render(request, "reception/dashboard.html", context)


@method_decorator(allow_manager_and_receptionist_only, name="dispatch")
class ReceptionHomeView(LoginRequiredMixin, View):
    # @method_decorator(allow_manager_and_receptionist_only)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = AddPatientForm()
        return render(request, "reception/home.html", {"form": form})

    def post(self, request):
        form = AddPatientForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            # set the receptionist to the currently logged in user.
            form.instance.receptionist = request.user
            form.save()
            form.save_m2m()
            messages.success(request, "Success")
            return redirect("reception_home")


class PatientDetailAndEditView(LoginRequiredMixin, View):
    """
    Handle viewing patients details on the detail page and also
    saving edited patients details.
    """

    @method_decorator(allow_manager_and_receptionist_only)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
    return render(request, "reception/search.html", context)
