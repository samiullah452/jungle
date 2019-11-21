from django.shortcuts import render


# Settings Page Views ....
def settings_views(request):
    context={
        'section' : 'settings'
    }
    return render(request, 'JungleScout_Settings_App/settings_page.html' , context)