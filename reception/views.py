from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse

from patients.models import Patient
from .forms import CreateReceptionistForm, AddPatient
from django.views import generic

import datetime


def create_receptionist(request):
    if request.method == 'POST':
        form = CreateReceptionistForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account for {username} has been created.")
            return redirect('reception_home')
    else:
        form = CreateReceptionistForm()
    context = {'form':form}
    return render(request, 'reception/create_receptionist.html', context)

def add_patient(request):
    if request.method == "POST":
        form = AddPatient(request.POST)
        if form.is_valid():
            form.save(commit=False)
            # this lambda function is going to strip the items that makes 
            # the tests_to_carry field a string and then convert the
            # newly formatted string into a list.
            # x = lambda x: x.replace('["','').replace(']"', '').strip()
            # form.instance.tests_to_carry = [x(form.instance.tests_to_carry)]
            form.instance.receptionist = request.user
            form.save()
            messages.success(request, "Success")
            return redirect('reception_home')
    else:
        form = AddPatient()
    return render(request, 'reception/home.html', {'form': form})

def dashboard(request):
    # get all the patients that were added to the database on a particular
    # day.
    # Will be extended to view all patients that were admitted on every 
    # particular day.

    # get the date inputed by the receptionist and then pass it in the filer
    # method
    # the dashboard will hold values that were added on that particular
    # day.
    today = datetime.date.today().isoformat()
    patients = Patient.objects.filter(date_added=today, receptionist=request.user)
    context = {'patients': patients} 
    return render(request, 'reception/dashboard.html', context)


class EditPatientInfoView(SuccessMessageMixin, generic.UpdateView):
    model = Patient
    fields = ['patients_name', 'patients_age']
    template_name = 'reception/patient_form.html'
    # success_url = reverse(dashboard)
    success_message = "Patient info has been updated successfully"

    def get_success_url(self):
        return reverse('dashboard')