from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import Group

from reception.forms import CreateReceptionistForm
from .decorators import allow_unauthenticated_only, allow_authenticated_only

from utils.decorators import allow_manager_only


@allow_unauthenticated_only
def login_user(request):
    """
    Login a user and then redirect to the homepage from were the user
    is then redirected to the appropriate view.
    """
    if request.method == "POST":
        email = request.POST.get("email_address")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("homepage")
        messages.error(request, "Username or Password incorrect")

    return render(request, "accounts/login.html")


@allow_manager_only
def register(request):
    form = CreateReceptionistForm()
    if request.method == "POST":
        form = CreateReceptionistForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user.groups.add(Group.objects.get(name="reception"))
            user.is_worker = True
            user.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Account Created for {username}")
            return redirect("login")
    context = {"form": form}
    return render(request, "accounts/register.html", context)


@allow_authenticated_only
def logout_user(request):
    """
    Logout a user and redirect to the login page.
    """
    logout(request)
    return redirect("login")
