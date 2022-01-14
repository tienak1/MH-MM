'''Photo app generic views'''
from django.shortcuts import get_object_or_404

from django.core.exceptions import PermissionDenied

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy

from .models import Photo
from .forms import ShareForm

# from .AES_cipher import AESCipher
from .AES import AESCipher, Matrix, DecryptImg
# from django.contrib.auth.models import User

import base64
from PIL import Image 
import io


class PhotoListView(ListView):
    
    model = Photo

    template_name = 'photoapp/list.html'

    def get_queryset(self):
        return self.model.objects.filter(submitter=self.request.user)
        
    context_object_name = 'photos'

    def get_context_data(self, **kwargs):
        context = super(PhotoListView, self).get_context_data(**kwargs)
        for photo in context["photos"]:
            photo.img = photo.image.url
        return context


class MyPhotoListView(PhotoListView):
    
    template_name = 'photoapp/myList.html'

    def get_queryset(self):
        return self.model.objects.filter(submitter=self.request.user)

class SharedWithMePhotoListView(PhotoListView):
    
    template_name = 'photoapp/sharedList.html'

    def get_queryset(self):
        return self.model.objects.filter(shared=self.request.user)

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
     

class DecryptionView(PhotoListView):

    template_name = 'photoapp/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for photo in context["photos"]:
            decoded_img = DecryptImg(photo)
            photo.img = f"data:image/jpeg;base64,{decoded_img}"
        return context


class PhotoDetailView(DetailView):

    model = Photo

    template_name = 'photoapp/detail.html'

    context_object_name = 'photo'
    
    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(PhotoDetailView, self).get_context_data(**kwargs)
        photo = self.get_photo()
        # Ikey = Matrix.string2matrix(photo.key)
        # cipher = AESCipher()
        # img_data = cipher.img_decrypt(photo.image.path, Ikey)
        # #img_data = Image.open(self.get_photo().image.path)
        # data = io.BytesIO()
        # img_data.save(data, "PNG")
        # encoded_img = base64.b64encode(data.getvalue())
        # decoded_img = encoded_img.decode('utf-8')
        decoded_img = DecryptImg(photo)
        # print(decoded_img)
        #img = f"data:image/jpeg;base64,{decoded_img}"
        context["dec_img"] = decoded_img
        return context


class PhotoCreateView(LoginRequiredMixin, CreateView):

    model = Photo
    
    fields = ['title', 'description', 'image', 'tags']

    template_name = 'photoapp/create.html'
    
    success_url = reverse_lazy('photo:list')   
    
    def form_valid(self, form):
        form.instance.submitter = self.request.user

        key, L, U = Matrix.Generate_IMatrix(20)
        # global Ikey, cipher
        Ikey =  Matrix.Find_IMatrix(L, U)
        Ikey = Matrix.matrix2string(Ikey)
        form.instance.key = Ikey
        cipher = AESCipher()
        cipher.img_encrypt(self.request.FILES['image'], key)
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

class PhotoShareView(UserIsSubmitter, UpdateView):
    
    template_name = 'photoapp/share.html'

    model = Photo

    form_class = ShareForm

    success_url = reverse_lazy('photo:list')
