from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import LabTests
from utils.decorators import allow_manager_only


def search_for_test(request):
    """
    Search for a particular test using the name to get the data about
    it(ie. the name and price)
    """
    query = request.GET["query"]
    test = LabTests.objects.filter(name__icontains=query)
    return render(request, "services/search.html", {"test": test})


@method_decorator(cache_page(30 * 60), name="dispatch")
class LabTestsListView(ListView):
    model = LabTests
    template_name = "services/listtests.html"


@method_decorator(allow_manager_only, name="dispatch")
class AddTestView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = LabTests
    fields = ["name", "price"]
    template_name = "services/labtest_form.html"
    success_message = "Added successfully"

    def form_valid(self, form):
        return super().form_valid(form)


@method_decorator(allow_manager_only, name="dispatch")
class EditTestView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = LabTests
    fields = ["name", "price"]
    template_name = "services/labtest_form.html"
    success_message = "Edited successfully"

    def form_valid(self, form):
        return super().form_valid(form)


@allow_manager_only
def delete_test(request, pk):
    test_to_delete = get_object_or_404(LabTests, pk=pk)
    test_to_delete.delete()
    return redirect("list_tests")
