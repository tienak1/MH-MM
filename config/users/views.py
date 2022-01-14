from django.views.generic import CreateView

from django.contrib.auth import authenticate, login

from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy

from cipher.RSA import CreateKey

from .models import UserKey
class SignUpView(CreateView):

    template_name = 'users/signup.html'
    
    form_class = UserCreationForm

    model = UserKey

    success_url = reverse_lazy('photo:myList')

    def form_valid(self, form):
        E, D, N = CreateKey()
        user = form.save()
        user.refresh_from_db() 
        hashD = hash(D)
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

        return to_return
    
class CustomLoginView(LoginView):
    
    template_name = 'users/login.html'
