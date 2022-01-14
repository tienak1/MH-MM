from audioop import reverse
from typing import ValuesView
from django.views.generic import CreateView, TemplateView

from django.contrib.auth import authenticate, login

from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy

from cipher.RSA import CreateKey

from .models import UserKey

import hashlib

class SignUpView(CreateView):

    template_name = 'users/signup.html'
    
    form_class = UserCreationForm

    model = UserKey

    success_url = reverse_lazy('user:viewKey')

    def form_valid(self, form):
        E, D, N = CreateKey()
        user = form.save()
        user.refresh_from_db() 
        hashD = hashlib.md5(bytes(D + 50)).hexdigest()
        user.userkey.D = hashD
        user.userkey.E = E
        user.userkey.N = N
        user.save()
        to_return = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        self.request.session["key"] = D
        return to_return

class KeyView(TemplateView):
    template_name = 'users/viewKey.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        D = self.request.session["key"]
        print(D)
        context["D"] = D
        return context

class CustomLoginView(LoginView):
    
    template_name = 'users/login.html'
