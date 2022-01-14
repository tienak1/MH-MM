'''Photo app Forms'''
from django import forms
from django.contrib.auth import get_user_model
from .models import Photo

class UserModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.id,obj.username)

class ShareForm(forms.ModelForm):
    share = UserModelChoiceField(queryset=get_user_model().objects.all().defer('submitter').prefetch_related('shared_users'),\
        widget = forms.CheckboxSelectMultiple(), required = False)

    class Meta:
        model = Photo
        fields = ['share']