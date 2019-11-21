from django import template
from mysite.models import *
from django.contrib.auth.models import User

register = template.Library()


def FindProfileImage(user_value):
    try:
        profile = profilePicture.objects.get(user = user_value)
        return profile.profileImage
    except:
        return False

register.filter(FindProfileImage)