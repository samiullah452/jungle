from django import template
from mysite.models import *
from django.contrib.auth.models import User

register = template.Library()


def FindProfileImageHeight(user_value):
    try:
        profile = profilePicture.objects.get(user = user_value)
        return profile.profileImage.height
    except:
        return False

register.filter(FindProfileImageHeight)