from django.db.models.signals import pre_save
from django.contrib.auth.models import User

def updateUser(sender,obj,**kwargs):

    user = obj
    if user.email != '':
        user.username = user.email

pre_save(updateUser,sender=User)