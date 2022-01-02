'''Photo app generic views'''
from django.shortcuts import render
from django.db import models
from django.shortcuts import get_object_or_404

from django.core.exceptions import PermissionDenied

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy
from .models import Photo

<<<<<<< Updated upstream
from .AES_cipher import AESCipher

=======
#from .AES_cipher import AESCipher
from django.utils.decorators import method_decorator
#from .uploadhandler import EncryptedFileUploadHandler
from django.views.decorators.csrf import csrf_exempt, csrf_protect
>>>>>>> Stashed changes
from django.contrib.auth.models import User

class PhotoListView(ListView):
    
    model = Photo

    template_name = 'photoapp/list.html'

    context_object_name = 'photos'


class PhotoTagListView(PhotoListView):
    
    template_name = 'photoapp/taglist.html'
    
    # Custom function
    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context
     

class PhotoDetailView(DetailView):

    model = Photo

    template_name = 'photoapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = User.objects.all()
        return context

    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):

    model = Photo
    
    fields = ['title', 'description', 'image', 'tags']

    template_name = 'photoapp/create.html'
    
    success_url = reverse_lazy('photo:list')   
    
    def form_valid(self, form):
        form.instance.submitter = self.request.user

        key = 'y6lLepZQpppdzjkeG5MhUaaaRCychpDd'
        cipher = AESCipher(key)
        cipher.encrypt(self.request.FILES['image'])

        form.save()
        return super().form_valid(form)

    

    

class UserIsSubmitter(UserPassesTestMixin):

    # Custom method
    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))
    
    def test_func(self):
        
        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')

class PhotoUpdateView(UserIsSubmitter, UpdateView):
    
    template_name = 'photoapp/update.html'

    model = Photo

    fields = ['title', 'description', 'tags']
    
    success_url = reverse_lazy('photo:list')

class PhotoDeleteView(UserIsSubmitter, DeleteView):
    
    template_name = 'photoapp/delete.html'

    model = Photo

    success_url = reverse_lazy('photo:list')

def PhotoShare(resquest):
    print(resquest.POST)