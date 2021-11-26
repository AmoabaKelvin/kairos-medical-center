from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def redirect_to_appropriate_view(function):
    """Return a user to the appropriate view upon visiting the homepage

    Args:
        function (function): The view function to decorate.
    """

    def wrapper(request, *args, **kwargs):
        if request.user.groups.exists():
            # a user can only belong to one group
            group = request.user.groups.all()[0].name
            if group == "reception":
                return redirect("reception_home")
            elif group == "manager":
                return redirect("management")

    return wrapper


def allow_receptionist_only(view_function):
    def wrapper(request, *args, **kwargs):
        has_group = request.user.groups.exists()
        if has_group and request.user.groups.all()[0].name == "reception":
            return view_function(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    return wrapper


def allow_manager_and_receptionist_only(view_function):
    def wrapper(request, *args, **kwargs):
        has_group = request.user.groups.exists()
        allowed = [i.name for i in request.user.groups.all()]
        print(allowed)
        if has_group and "manager" or "reception" in allowed:
            return view_function(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    return wrapper
