from django.shortcuts import redirect
from django.urls import reverse


def allow_unauthenticated_only(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("homepage"))
        else:
            return view_function(request, *args, **kwargs)

    return wrapper


def allow_authenticated_only(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_function(request, *args, **kwargs)
        else:
            return redirect("login")

    return wrapper
