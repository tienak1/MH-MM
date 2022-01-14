from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserKey(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    #other fields here
    E = models.BigIntegerField(null=True)
    N = models.BigIntegerField(null=True)
    D = models.BigIntegerField(null=True)
    def __str__(self):  
          return self.D

@receiver(post_save, sender=User)
def create_user_key(sender, instance, created, **kwargs):  
    if created:  
       UserKey.objects.create(user=instance)
    instance.userkey.save()
