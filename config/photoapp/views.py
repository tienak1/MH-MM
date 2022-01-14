'''Photo app generic views'''
from urllib import request
from django.shortcuts import get_object_or_404

from django.core.exceptions import PermissionDenied

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, RedirectView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy, reverse

from .models import Photo
from .forms import ShareForm
from cipher.AES import AESCipher, Matrix, DecryptImg
from cipher.RSA import RSA, checkHash
from .forms import privateKeyForm

from django.shortcuts import render


class PhotoListView(ListView):
    
    model = Photo

    template_name = 'photoapp/list.html'

    context_object_name = 'photos'

    def get_context_data(self, **kwargs):
        context = super(PhotoListView, self).get_context_data(**kwargs)
        for photo in context["photos"]:
            photo.img = photo.image.url
        return context

class MyPhotoListView(PhotoListView):
    def get_queryset(self):
        return self.model.objects.filter(submitter=self.request.user)
        
class SharedWithMePhotoListView(PhotoListView):

    def get_queryset(self):
        return self.model.objects.filter(share__username=self.request.user)


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
     

class DecryptionView(MyPhotoListView):

    template_name = 'photoapp/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        D = self.request.session["D"]
        for photo in context["photos"]:
            decoded_img = DecryptImg(photo, D)
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
        D = self.request.session["D"]
        photo = self.get_photo()
        decoded_img = DecryptImg(photo, D)
        context["dec_img"] = decoded_img
        return context


class PhotoCreateView(LoginRequiredMixin, CreateView):

    model = Photo
    
    fields = ['title', 'description', 'image', 'tags']

    template_name = 'photoapp/create.html'
    
    success_url = reverse_lazy('photo:myList')   
    
    def form_valid(self, form):
        form.instance.submitter = self.request.user
        E = self.request.user.userkey.E
        N = self.request.user.userkey.N
        key, L, U = Matrix.Generate_IMatrix(20)
        # global Ikey, cipher
        Ikey =  Matrix.Find_IMatrix(L, U)
        RSA_cipher = RSA()
        Ikey = RSA_cipher.encrypt(Ikey, E, N)
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
    
    success_url = reverse_lazy('photo:myList')

class PhotoDeleteView(UserIsSubmitter, DeleteView):
    
    template_name = 'photoapp/delete.html'

    model = Photo

    success_url = reverse_lazy('photo:myList')

class PhotoShareView(UserIsSubmitter, UpdateView):
    
    template_name = 'photoapp/share.html'

    model = Photo

    form_class = ShareForm

    success_url = reverse_lazy('photo:myList')

def privateKey(request):
    context = {}
    context['form'] = privateKeyForm()
    return render( request, "photoapp/privateKey.html", context)

class PrivateKeyView(FormView, RedirectView):
    template_name = "photoapp/privateKey.html"

    form_class = privateKeyForm
    
    def get_success_url(self, **kwargs):
        self.photo = self.kwargs.get('pk')
        print(self.photo)
        D_input = int(self.request.POST["key"])
        D_hash = self.request.user.userkey.D
        check = checkHash(D_input, D_hash)
        if check:
            self.request.session["D"]=D_input
            if self.photo:
                return reverse("photo:detail", kwargs={"pk": self.photo})
            else:
                return reverse("photo:decryptedList")
        else:
            reverse_lazy('photo:myList')

    # success_url = get_redirect_url()