import datetime

from django.views.generic.base import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from patients.models import Patient
from patients.forms import AddPatientForm, EditPatientInfoForm
from utils.decorators import allow_manager_and_receptionist_only


@login_required(login_url="login")
@allow_manager_and_receptionist_only
def dashboard(request):
    """
    Get all the patients that were added to the database on a particular
    day and were entered by the currently logged in receptionist.
    """
    today = datetime.date.today().isoformat()
    if request.user.is_manager():
        patients = Patient.objects.filter(date_added=today)
    else:
        patients = Patient.objects.filter(date_added=today, receptionist=request.user)
    context = {"patients": patients}
    return render(request, "reception/dashboard.html", context)


@method_decorator(allow_manager_and_receptionist_only, name="dispatch")
class ReceptionHomeView(LoginRequiredMixin, View):
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
        else:
            return render(request, "reception/home.html", {"form": form})


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
        else:
            return render(request, "reception/patient_detail_and_edit.html")
