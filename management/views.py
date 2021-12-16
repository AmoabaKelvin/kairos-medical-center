import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from customuser.models import CustomUser
from patients.models import Patient
from utils.decorators import allow_manager_only, allow_manager_and_receptionist_only


@login_required
@allow_manager_and_receptionist_only
def days_summary(request):
    """
    Get the Number of tests done and then compute the prices.
    """
    if request.GET.get("date-picker") is not None:
        date = request.GET["date-picker"]
        patient = Patient.get_todays_test_summary(date_added=date)
    else:
        patient = Patient.get_todays_test_summary()
    context = {"results": patient}

    return render(request, "reception/days_summary.html", context)


@login_required
@allow_manager_only
def homepage(request):
    patient = Patient.get_todays_test_summary()
    total_workers = CustomUser.objects.filter(is_worker=True).count()
    tests_performed, cost = Patient.tests_performed_today()
    # get the patients that were added today
    patients_today = Patient.objects.filter(
        date_added=datetime.date.today().isoformat()
    ).count()
    context = {
        "total_workers": total_workers,
        "tests_performed": tests_performed,
        "patients_today": patients_today,
        "cost": cost,
        "results": patient,
    }

    return render(request, "index.html", context)


@login_required
@allow_manager_only
def get_current_workers(request):
    workers = CustomUser.objects.filter(is_worker=True)
    context = {"workers": workers}

    return render(request, "management/workers.html", context)
