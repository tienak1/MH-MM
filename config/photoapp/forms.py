'''Photo app Forms'''
from django import forms
from django.contrib.auth import get_user_model
from .models import Share

class UserModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.id,obj.username)

class ShareForm(forms.ModelForm):
    user = UserModelChoiceField(queryset=get_user_model().objects.all(),\
        widget = forms.CheckboxSelectMultiple(), required = False)
    # def __init__(self, *args, **kwargs):
    #     super(ShareForm, self).__init__(*args, **kwargs)
    #     self.fields['photo'] = kwargs.pop('photo')
    #     self.fields['user'] = forms.ModelChoiceField(label="User", choices=[(x.plug_ip, x.id) for x in get_user_model().objects.all()])
    
    class Meta:
        model = Share
        exclude = ['photo']