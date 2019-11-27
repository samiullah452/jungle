from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

urlpatterns = [
    # Home URL (Product Tracker Page)
    url(r'^$' , views.home, name="home"),

    # Keyword Scrapper URL ...
    url(r'profitcalculator/$', views.profitcalculator, name="profitcalculator"),
    url(r'^keyword/$', views.keyword_view, name="keyword"),
    url(r'^keyword-find/$', views.keyword_find, name="keyword_find"),
    url(r'^content-downloader/$', views.content_downloader, name="content_downloader"),
    url(r'^supplier-finder/$', views.supplier_finder, name="supplier-finder"),
    url(r'^supplier-find/$', views.supplier_find, name="supplier-find"),

    # Register URL
    url(r'^register/$', views.register_user, name= "register"),

    # Email Confirm URL
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),

    # Login URL
    url(r'login/$', views.login_user, name = 'login'),

    # Logout URL
    url(r'^logout/$', views.logout_user, name= "logout"),

    # Password Reset URLs
    path('password_reset/', PasswordResetView.as_view(), name='password_reset' ),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Profile Visit URL
    url(r'^profile/$', views.profile_user, name= "profile"),
    
    #Password Change URL
    url(r'^change_password/$', views.change_password, name = "change_password"),

    # Delete Profile Image URL
    url(r'^remove-profile-image/$', views.delete_profileImage, name="delete-profile" ),

    # Update Profile Image URL
    url(r'update-profile-image/$', views.upload_profileImage, name="upload-profile-image"),
    url(r'^del_user/$', views.del_user,name="del_user"), 

]
