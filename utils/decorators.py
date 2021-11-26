from django.http import HttpResponseForbidden


def allow_manager_only(view_function):
    def wrapper(request, *args, **kwargs):
        has_group = request.user.groups.exists()
        if has_group and request.user.groups.all()[0].name != "manager":
            return HttpResponseForbidden()
        else:
            return view_function(request, *args, **kwargs)
    return wrapper
            