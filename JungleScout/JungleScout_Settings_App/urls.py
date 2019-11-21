from django.conf.urls import url

from . import views

urlpatterns = [
    # Settings Page URL ...
    url(r'^$', views.settings_views, name="settings_page")
]