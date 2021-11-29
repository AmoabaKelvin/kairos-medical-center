from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from django.core.mail import EmailMessage
from .forms import SendEmailForm
from django.urls import reverse

# Create your views here.
class SendMailForm(FormView):
    template_name = 'common/send_mail.html'
    success_url =  'mail'
    form_class = SendEmailForm

    def get_success_url(self) -> str:
        return reverse('send_mail')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


def mail(request):
    form = SendEmailForm()
    print(form.is_valid())
    if request.method == "POST": 
        form = SendEmailForm(request.POST, request.FILES)
        print(f"Entered post {form.is_valid()}")
        print(form.errors)
        if form.is_valid():
            # form = SendEmailForm(request.POST, request.FILES)
            # recipient = form.cleaned_data.get("recipient")
            # message = form.cleaned_data.get("message")
            # file = form.files["attachment"]
            # print(recipient)
            # print(message)
            # print(file)
            form.send_email()
            return HttpResponse("Sent")
        else:
            form = SendEmailForm()
    return render(request, 'common/send_mail.html', {"form":form})