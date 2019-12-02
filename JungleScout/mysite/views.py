from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import *
from .models import *
from django.core.files.base import ContentFile
from django.core.files import *
from django.core.files.images import ImageFile
import os
import re
from contentdownloader.contentdownloader import content
from SupplierFinders.supplier import supplier
from kyword.keyword import keyword_finder
from profitcalculator.profitcal import profitcal
import json
from django.core.files.storage import FileSystemStorage

# Content Downlaoder view
def keyword_find(request):
    if request.method == 'GET':

        if request.GET.get('delete'):
            user_keywords.objects.filter(id=request.GET.get('delete')).delete()

        if request.GET.get('move'):
            user_keywords.objects.filter(id=request.GET.get('move')).update(name=keyword_groups.objects.get(user=request.user,name=request.GET.get('group')))

        if request.GET.get('edit'):

            if request.GET.get('field')=='Category Name':
                user_keywords.objects.filter(id=request.GET.get('edit')).update(category_name=request.GET.get('data'))
            if request.GET.get('field')=='Category Id':
                user_keywords.objects.filter(id=request.GET.get('edit')).update(category_id=request.GET.get('data'))
            if request.GET.get('field')=='Title':
                user_keywords.objects.filter(id=request.GET.get('edit')).update(product_name=request.GET.get('data'))
            if request.GET.get('field')=='Description':
                user_keywords.objects.filter(id=request.GET.get('edit')).update(details=request.GET.get('data'))

        if request.GET.get('create'):
            keyword_groups(name=request.GET.get('create'),user=request.user).save()

        if request.GET.get('groupdelete'):
            keyword_groups.objects.filter(name=request.GET.get('groupdelete'),user=request.user).delete()

        if request.GET.get('edit_key'):
            user_keywords.objects.filter(id=request.GET.get('edit_key')).update(keywords=request.GET.get('data'))

        if request.GET.get('editgroup'):
            keyword_groups.objects.filter(name=request.GET.get('editgroup'),user=request.user).update(name=request.GET.get('data'))

        return HttpResponse(json.dumps('Success'), content_type='application/json')       

    if request.method == 'POST':
        if request.POST.getlist('deleteselected[]'):
            user_keywords.objects.filter(id__in=request.POST.getlist('deleteselected[]')).delete()
            return HttpResponse(json.dumps('Success'), content_type='application/json')       

        if request.POST.getlist('moveselected[]'):
            user_keywords.objects.filter(id__in=request.POST.getlist('moveselected[]')).update(name=keyword_groups.objects.get(user=request.user,name=request.POST.get('group')))
            return HttpResponse(json.dumps('Success'), content_type='application/json')       

        Urls=request.POST.getlist('urls[]')
        sup=keyword_finder(Urls)        
        try:
            keyword_groups.objects.get(user=request.user,name="Uncategorized")
        except keyword_groups.DoesNotExist:
            grp=keyword_groups(user=request.user,name="Uncategorized")
            grp.save()
        for key in sup.keys(): 
            t=user_keywords(category_name=sup[key]['category_name'],product_name=sup[key]['title'],category_id=sup[key]['category_id'],name=keyword_groups.objects.get(name='Uncategorized',user=request.user),details=sup[key]['description'],url=sup[key]['url'],keywords=sup[key]['keywords']) 
            t.save()
            sup[key]['id']=t.id
        return HttpResponse(json.dumps(sup), content_type='application/json')


def testing(request):
    from testing.testing import test
    if request.method == 'POST' and request.is_ajax():
        website=request.POST.get('website')
        file_names=[]
        if 'file[]' in request.FILES:
            file = request.FILES.getlist('file[]')
            for myfile in file:
                fs = FileSystemStorage(settings.MEDIA_ROOT)
                filename = fs.save(myfile.name, myfile)
                if website !="Alibaba":
                        file_names.append("http://138.197.67.53:8000"+"/media/1.PNG")
                else:
                        file_names.append(settings.MEDIA_ROOT+"/"+filename)
        test=test(file_names,website)
        i=0
        for key in test.keys(): 
                test[key]['id']=i
                i+=1
        print(test)
        return HttpResponse(json.dumps(test), content_type='application/json')
    if request.user.is_authenticated:
        return render(request,'mysite/testing.html')
    context={
        'section' : 'findProduct'
    }
    return render(request, 'mysite/homebeforeLogin.html' , context)

def profitcalculator(request):
    if request.method == 'GET' and request.is_ajax():

        if request.GET.get('delete'):
            user_profit.objects.filter(id=request.GET.get('delete')).delete()

        if request.GET.get('move'):
            user_profit.objects.filter(id=request.GET.get('move')).update(name=profit_groups.objects.get(user=request.user,name=request.GET.get('group')))

        if request.GET.get('create'):
            profit_groups(name=request.GET.get('create'),user=request.user).save()

        if request.GET.get('groupdelete'):
            profit_groups.objects.filter(name=request.GET.get('groupdelete'),user=request.user).delete()

        if request.GET.get('edit'):
            user_profit.objects.filter(id=request.GET.get('edit')).update(keywords=request.GET.get('new_keywords'))

        return HttpResponse(json.dumps('Success'), content_type='application/json')           

    if request.method == 'POST' and request.is_ajax():
        if request.POST.get('calculate'):
            create=False
            if request.POST.get('id') is not None:
                user_profit.objects.filter(id=request.POST.get('id')).update(product_name=request.POST.get('product_name'),
                    selling_price_max=float(request.POST.get('sel_max')),
                    selling_price_min=float(request.POST.get('sel_min')),
                    selling_price_avg=float(request.POST.get('sel_avg')),
                    china_price_min=float(request.POST.get('china_min')),
                    china_price_avg=float(request.POST.get('china_avg')),
                    china_price_max=float(request.POST.get('china_max')),
                    exchange_rate=float(request.POST.get('exchange')),
                    oversea_shipping=float(request.POST.get('shipping')),
                    tax_rate=float(request.POST.get('tax_rate')),
                    vat=float(request.POST.get('vat')),
                    local_delievery_cost=float(request.POST.get('local')),
                    extra_cost=float(request.POST.get('extra'))
                    )
                t=user_profit.objects.get(id=request.POST.get('id'))
                create=False
            else:
                    t=user_profit(product_name=request.POST.get('product_name'),
                    selling_price_max=float(request.POST.get('sel_max')),
                    selling_price_min=float(request.POST.get('sel_min')),
                    selling_price_avg=float(request.POST.get('sel_avg')),
                    china_price_min=float(request.POST.get('china_min')),
                    china_price_avg=float(request.POST.get('china_avg')),
                    china_price_max=float(request.POST.get('china_max')),
                    exchange_rate=float(request.POST.get('exchange')),
                    oversea_shipping=float(request.POST.get('shipping')),
                    tax_rate=float(request.POST.get('tax_rate')),
                    vat=float(request.POST.get('vat')),
                    local_delievery_cost=float(request.POST.get('local')),
                    extra_cost=float(request.POST.get('extra'))
                    )
                    t.save()
                    create=True

            profs={}
            key=0
		
            total_cost_min=(t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate+(t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat+(t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)
            total_cost_max=(t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate+(t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat+(t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)
            total_cost_avg=(t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate+(t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat+(t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)
            
            total_cost1_min=(t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)
            total_cost1_max=(t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)
            total_cost1_avg=(t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)	

            net_profit_min=(t.selling_price_min-t.local_delievery_cost)-total_cost_min-((t.selling_price_min-t.local_delievery_cost)-total_cost_min)*t.vat
            net_profit_max=(t.selling_price_max-t.local_delievery_cost)-total_cost_max-((t.selling_price_max-t.local_delievery_cost)-total_cost_max)*t.vat
            net_profit_avg=(t.selling_price_avg-t.local_delievery_cost)-total_cost_avg-((t.selling_price_avg-t.local_delievery_cost)-total_cost_avg)*t.vat

            profs[key]={}
            profs[key]['Group']="Uncategorized"
            profs[key]['Title']=t.product_name
            profs[key]['china-price']=str(t.china_price_min)+','+str(t.china_price_avg)+','+str(t.china_price_max)
            profs[key]['exchange_rate']=t.exchange_rate
            profs[key]['Currency']=str(t.china_price_min*t.exchange_rate)+','+str(t.china_price_avg*t.exchange_rate)+','+str(t.china_price_max*t.exchange_rate)
            profs[key]['shipping']=str(t.oversea_shipping)
            profs[key]['extra_cost']=t.extra_cost
            profs[key]['total-cost']=str(total_cost1_min)+','+str(total_cost1_avg)+','+str(total_cost1_max)
            profs[key]['tax_rate']=t.tax_rate
            profs[key]['tax_rate1']=str((t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate)+','+str((t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate)+','+str((t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate)
            profs[key]['vat']=t.vat
            profs[key]['vat1']=str((t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat)+','+str((t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat)+','+str((t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat)
            profs[key]['final-cost']=str(total_cost_min)+','+str(total_cost_avg)+','+str(total_cost_max)
            profs[key]['selling_price']=str(t.selling_price_min)+','+str(t.selling_price_avg)+','+str(t.selling_price_max)
            profs[key]['local']=t.local_delievery_cost
            profs[key]['consumer_price']=str(t.selling_price_min-t.local_delievery_cost)+','+str(t.selling_price_avg-t.local_delievery_cost)+','+str(t.selling_price_max-t.local_delievery_cost)
            profs[key]['final_vat']=str(((t.selling_price_min-t.local_delievery_cost)-total_cost_min)*t.vat)+','+str(((t.selling_price_avg-t.local_delievery_cost)-total_cost_avg)*t.vat)+','+str(((t.selling_price_max-t.local_delievery_cost)-total_cost_max)*t.vat)
            profs[key]['net profit']=str(net_profit_min)+','+str(net_profit_avg)+','+str(net_profit_max)
            profs[key]['id']=t.id
    
            return HttpResponse(json.dumps([create,profs,t.id]), content_type='application/json')

        website=request.POST.get('website')
        file_names=[]
        if 'file[]' in request.FILES:
            file = request.FILES.getlist('file[]')
            for myfile in file:
                fs = FileSystemStorage(settings.MEDIA_ROOT)
                filename = fs.save(myfile.name, myfile)
                file_names.append(settings.MEDIA_ROOT+"/"+filename)
        
        keys=request.POST.getlist('keys[]')
        prof=profitcal(file_names,website,keys)
        profs={}
        try:
            profit_groups.objects.get(user=request.user,name="Uncategorized")
        except profit_groups.DoesNotExist:
            grp=profit_groups(user=request.user,name="Uncategorized")
            grp.save()
        for key in prof.keys(): 
            t=user_profit(china_price_avg=prof[key]['avg'],china_price_min=prof[key]['min'],china_price_max=prof[key]['max'],product_name=prof[key]['title'],key=prof[key]['key'],name=profit_groups.objects.get(name='Uncategorized',user=request.user)) 
            total_cost_min=(t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate+(t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat+(t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)
            total_cost_max=(t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate+(t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat+(t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)
            total_cost_avg=(t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate+(t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat+(t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)

            total_cost1_min=(t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)
            total_cost1_max=(t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)
            total_cost1_avg=(t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)	
		
            t.selling_price_min=total_cost_min
            t.selling_price_avg=total_cost_avg
            t.selling_price_max=total_cost_max
            t.save()
            net_profit_min=(t.selling_price_min-t.local_delievery_cost)-total_cost_min-((t.selling_price_min-t.local_delievery_cost)-total_cost_min)*t.vat
            net_profit_max=(t.selling_price_max-t.local_delievery_cost)-total_cost_max-((t.selling_price_max-t.local_delievery_cost)-total_cost_max)*t.vat
            net_profit_avg=(t.selling_price_avg-t.local_delievery_cost)-total_cost_avg-((t.selling_price_avg-t.local_delievery_cost)-total_cost_avg)*t.vat

            profs[key]={}
            profs[key]['Group']="Uncategorized"
            profs[key]['Title']=t.product_name
            profs[key]['china-price']=str(prof[key]['min'])+','+str(prof[key]['avg'])+','+str(prof[key]['max'])
            profs[key]['exchange_rate']=t.exchange_rate
            profs[key]['Currency']=str(t.china_price_min*t.exchange_rate)+','+str(t.china_price_avg*t.exchange_rate)+','+str(t.china_price_max*t.exchange_rate)
            profs[key]['shipping']=str(t.oversea_shipping)
            profs[key]['extra_cost']=t.extra_cost
            profs[key]['total-cost']=str(total_cost1_min)+','+str(total_cost1_avg)+','+str(total_cost1_max)
            profs[key]['tax_rate']=t.tax_rate
            profs[key]['tax_rate1']=str((t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate)+','+str((t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate)+','+str((t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate)
            profs[key]['vat']=t.vat
            profs[key]['vat1']=str((t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat)+','+str((t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat)+','+str((t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat)
            profs[key]['final-cost']=str(total_cost_min)+','+str(total_cost_avg)+','+str(total_cost_max)
            profs[key]['selling_price']=str(t.selling_price_min)+','+str(t.selling_price_avg)+','+str(t.selling_price_max)
            profs[key]['local']=t.local_delievery_cost
            profs[key]['consumer_price']=str(t.selling_price_min-t.local_delievery_cost)+','+str(t.selling_price_avg-t.local_delievery_cost)+','+str(t.selling_price_max-t.local_delievery_cost)
            profs[key]['final_vat']=str(((t.selling_price_min-t.local_delievery_cost)-total_cost_min)*t.vat)+','+str(((t.selling_price_avg-t.local_delievery_cost)-total_cost_avg)*t.vat)+','+str(((t.selling_price_max-t.local_delievery_cost)-total_cost_max)*t.vat)
            profs[key]['net profit']=str(net_profit_min)+','+str(net_profit_avg)+','+str(net_profit_max)
            profs[key]['id']=t.id
    
        return HttpResponse(json.dumps(profs), content_type='application/json')
    if request.user.is_authenticated:
        overview={}
        groups_show=[]
        Groups=profit_groups.objects.filter(user=request.user)
        i=0
        for grp in Groups:
            if grp.name!="Uncategorized":
                groups_show.append(grp.name)
            Overview=user_profit.objects.filter(name=grp)
            for over in Overview:
                overview[i]={}
                total_cost_min=(over.china_price_min*over.exchange_rate+over.extra_cost+over.oversea_shipping)*over.tax_rate+(over.china_price_min*over.exchange_rate+over.extra_cost+over.oversea_shipping)*over.vat+(over.china_price_min*over.exchange_rate+over.extra_cost+over.oversea_shipping)
                total_cost_max=(over.china_price_max*over.exchange_rate+over.extra_cost+over.oversea_shipping)*over.tax_rate+(over.china_price_max*over.exchange_rate+over.extra_cost+over.oversea_shipping)*over.vat+(over.china_price_max*over.exchange_rate+over.extra_cost+over.oversea_shipping)
                total_cost_avg=(over.china_price_avg*over.exchange_rate+over.extra_cost+over.oversea_shipping)*over.tax_rate+(over.china_price_avg*over.exchange_rate+over.extra_cost+over.oversea_shipping)*over.vat+(over.china_price_avg*over.exchange_rate+over.extra_cost+over.oversea_shipping)

                total_cost1_min=(over.china_price_min*over.exchange_rate+over.extra_cost+over.oversea_shipping)
                total_cost1_max=(over.china_price_max*over.exchange_rate+over.extra_cost+over.oversea_shipping)
                total_cost1_avg=(over.china_price_avg*over.exchange_rate+over.extra_cost+over.oversea_shipping)	

                net_profit_min=(over.selling_price_min-over.local_delievery_cost)-total_cost_min-((over.selling_price_min-over.local_delievery_cost)-total_cost_min)*over.vat
                net_profit_max=(over.selling_price_max-over.local_delievery_cost)-total_cost_max-((over.selling_price_max-over.local_delievery_cost)-total_cost_max)*over.vat
                net_profit_avg=(over.selling_price_avg-over.local_delievery_cost)-total_cost_avg-((over.selling_price_avg-over.local_delievery_cost)-total_cost_avg)*over.vat
                
                overview[i]['Group']=over.name.name
                overview[i]['Title']=over.product_name
                overview[i]['china-price']=str(over.china_price_min)+','+str(over.china_price_avg)+','+str(over.china_price_max)
                overview[i]['exchange_rate']=over.exchange_rate
                overview[i]['Currency']=str(over.china_price_min*over.exchange_rate)+','+str(over.china_price_avg*over.exchange_rate)+','+str(over.china_price_max*over.exchange_rate)
                overview[i]['shipping']=str(over.oversea_shipping)
                overview[i]['extra_cost']=over.extra_cost
                overview[i]['total-cost']=str(total_cost1_min)+','+str(total_cost1_avg)+','+str(total_cost1_max)
                overview[i]['tax_rate']=over.tax_rate
                overview[i]['tax_rate1']=str((over.china_price_min*over.exchange_rate+over.extra_cost+over.oversea_shipping)*over.tax_rate)+','+str((over.china_price_avg*over.exchange_rate+over.extra_cost+over.oversea_shipping)*over.tax_rate)+','+str((over.china_price_max*over.exchange_rate+over.extra_cost+over.oversea_shipping)*over.tax_rate)
                overview[i]['vat']=over.vat
                overview[i]['vat1']=str((over.china_price_min*over.exchange_rate+over.extra_cost+over.oversea_shipping)*over.vat)+','+str((over.china_price_avg*over.exchange_rate+over.extra_cost+over.oversea_shipping)*over.vat)+','+str((over.china_price_max*over.exchange_rate+over.extra_cost+over.oversea_shipping)*over.vat)
                overview[i]['final-cost']=str(total_cost_min)+','+str(total_cost_avg)+','+str(total_cost_max)
                overview[i]['selling_price']=str(over.selling_price_min)+','+str(over.selling_price_avg)+','+str(over.selling_price_max)
                overview[i]['local']=over.local_delievery_cost
                overview[i]['consumer_price']=str(over.selling_price_min-over.local_delievery_cost)+','+str(over.selling_price_avg-over.local_delievery_cost)+','+str(over.selling_price_max-over.local_delievery_cost)
                overview[i]['final_vat']=str(((over.selling_price_min-over.local_delievery_cost)-total_cost_min)*over.vat)+','+str(((over.selling_price_avg-over.local_delievery_cost)-total_cost_avg)*over.vat)+','+str(((over.selling_price_max-over.local_delievery_cost)-total_cost_max)*over.vat)
                overview[i]['net profit']=str(net_profit_min)+','+str(net_profit_avg)+','+str(net_profit_max)
                overview[i]['id']=over.id
                i+=1

        context={
        'overview':json.dumps(overview),
        'groups':groups_show,
        }

        return render(request,'mysite/profilcalculator.html',context)
    context={
        'section' : 'findProduct'
    }
    return render(request, 'mysite/homebeforeLogin.html' , context)
def content_downloader(request):

    if request.method == 'GET':

        if request.GET.get('delete'):
            user_content_downloader.objects.filter(id=request.GET.get('delete')).delete()

        if request.GET.get('move'):
            user_content_downloader.objects.filter(id=request.GET.get('move')).update(name=content_downloader_groups.objects.get(user=request.user,name=request.GET.get('group')))

        if request.GET.get('edit'):
            if request.GET.get('field')=='Store Name':
                user_content_downloader.objects.filter(id=request.GET.get('edit')).update(store_name=request.GET.get('data'))
            if request.GET.get('field')=='Product Name':
                user_content_downloader.objects.filter(id=request.GET.get('edit')).update(product_name=request.GET.get('data'))
            if request.GET.get('field')=='Details':
                user_content_downloader.objects.filter(id=request.GET.get('edit')).update(details=request.GET.get('data'))
            if request.GET.get('field')=='Price CNY':
                user_content_downloader.objects.filter(id=request.GET.get('edit')).update(price=request.GET.get('data'))
            if request.GET.get('field')=='Price KWON':
                user_content_downloader.objects.filter(id=request.GET.get('edit')).update(price_krw=request.GET.get('data'))


        if request.GET.get('create'):
            content_downloader_groups(name=request.GET.get('create'),user=request.user).save()

        if request.GET.get('groupdelete'):
            content_downloader_groups.objects.filter(name=request.GET.get('groupdelete'),user=request.user).delete()

        if request.GET.get('editgroup'):
            content_downloader_groups.objects.filter(name=request.GET.get('editgroup'),user=request.user).update(name=request.GET.get('data'))

        return HttpResponse(json.dumps('Success'), content_type='application/json')       

    if request.method == 'POST':
        if request.POST.getlist('deleteselected[]'):
            user_content_downloader.objects.filter(id__in=request.POST.getlist('deleteselected[]')).delete()
            return HttpResponse(json.dumps('Success'), content_type='application/json')       

        if request.POST.getlist('moveselected[]'):
            user_content_downloader.objects.filter(id__in=request.POST.getlist('moveselected[]')).update(name=content_downloader_groups.objects.get(user=request.user,name=request.POST.get('group')))
            return HttpResponse(json.dumps('Success'), content_type='application/json')       

        Urls=request.POST.getlist('urls[]')
        website=request.POST.get('website')
        cont=content(Urls,website)

        try:
            content_downloader_groups.objects.get(user=request.user,name="Uncategorized")
        except content_downloader_groups.DoesNotExist:
            grp=content_downloader_groups(user=request.user,name="Uncategorized")
            grp.save()
        for key in cont.keys(): 
            t=user_content_downloader(store_name=cont[key]['shop-name'],product_name=cont[key]['title'],price=cont[key]['price'],name=content_downloader_groups.objects.get(name='Uncategorized',user=request.user),details=cont[key]['details'],url=cont[key]['url'],image=cont[key]['image'],price_krw=cont[key]['price_krw']) 
            t.save()
            cont[key]['id']=t.id

        return HttpResponse(json.dumps(cont), content_type='application/json')

def supplier_find(request):
    if request.method == 'GET':
        if request.GET.get('edit'):
            if request.GET.get('field')=='Store Name':
                user_supplier_finder.objects.filter(id=request.GET.get('edit')).update(store_name=request.GET.get('data'))
            if request.GET.get('field')=='Product Name':
                user_supplier_finder.objects.filter(id=request.GET.get('edit')).update(product_name=request.GET.get('data'))
            if request.GET.get('field')=='Price CNY':
                user_supplier_finder.objects.filter(id=request.GET.get('edit')).update(price=request.GET.get('data'))
            if request.GET.get('field')=='Price KWON':
                user_supplier_finder.objects.filter(id=request.GET.get('edit')).update(price_krw=request.GET.get('data'))
            if request.GET.get('field')=='Location':
                user_supplier_finder.objects.filter(id=request.GET.get('edit')).update(region=request.GET.get('data'))

        if request.GET.get('delete'):
            user_supplier_finder.objects.filter(id=request.GET.get('delete')).delete()

        if request.GET.get('move'):
            user_supplier_finder.objects.filter(id=request.GET.get('move')).update(name=supplier_finder_groups.objects.get(user=request.user,name=request.GET.get('group')))

        if request.GET.get('create'):
            supplier_finder_groups(name=request.GET.get('create'),user=request.user).save()

        if request.GET.get('editgroup'):
           supplier_finder_groups.objects.filter(name=request.GET.get('editgroup'),user=request.user).update(name=request.GET.get('data'))

        if request.GET.get('groupdelete'):
            supplier_finder_groups.objects.filter(name=request.GET.get('groupdelete'),user=request.user).delete()

        return HttpResponse(json.dumps('Success'), content_type='application/json')       

    if request.method == 'POST':
    
        if request.POST.getlist('deleteselected[]'):
            user_supplier_finder.objects.filter(id__in=request.POST.getlist('deleteselected[]')).delete()
            return HttpResponse(json.dumps('Success'), content_type='application/json')       

        if request.POST.getlist('moveselected[]'):
            user_supplier_finder.objects.filter(id__in=request.POST.getlist('moveselected[]')).update(name=supplier_finder_groups.objects.get(user=request.user,name=request.POST.get('group')))
            return HttpResponse(json.dumps('Success'), content_type='application/json')       

        keys=request.POST.getlist('urls[]')
        website=request.POST.get('website')
        sup=supplier(keys,website)

        try:
            supplier_finder_groups.objects.get(user=request.user,name="Uncategorized")
        except supplier_finder_groups.DoesNotExist:
            grp=supplier_finder_groups(user=request.user,name="Uncategorized")
            grp.save()
        for key in sup.keys(): 
            t=user_supplier_finder(store_name=sup[key]['shop-name'],product_name=sup[key]['title'],price=sup[key]['price'],price_krw=sup[key]['price_krw'],name=supplier_finder_groups.objects.get(name='Uncategorized',user=request.user),region=sup[key]['region'],url=sup[key]['url']) 
            t.save()
            for img in sup[key]['image']:
                i=supplier_finder_image(src=img,supplier=t)
                i.save()
            sup[key]['id']=t.id
        return HttpResponse(json.dumps(sup), content_type='application/json')

def supplier_finder(request):
    if request.user.is_authenticated:
        overview={}
        groups_show=[]
        Groups=supplier_finder_groups.objects.filter(user=request.user)
        i=0
        for grp in Groups:
            groups_show.append(grp.name)
            Overview=user_supplier_finder.objects.filter(name=grp)
            for over in Overview:
              overview[i]={}
              overview[i]['id']=over.id
              overview[i]['group']=over.name.name
              overview[i]['shop-name']=over.store_name
              overview[i]['image']=[]
              images=supplier_finder_image.objects.filter(supplier=over)
              for image in images:
                overview[i]['image'].append(image.src)
              overview[i]['title']=over.product_name
              overview[i]['price']=over.price
              overview[i]['price_krw']=over.price_krw
              overview[i]['region']=over.region
              overview[i]['url']=over.url
              i+=1
        context={
        'overview':json.dumps(overview),
        'groups':groups_show,
            'section' : 'findProduct'
        }
        return render(request, 'mysite/supplier_finder.html', context)
    context={
        'section' : 'findProduct'
    }
    return render(request, 'mysite/homebeforeLogin.html' , context)
# Home View (Product Tracker) ...
def home(request):
    if request.user.is_authenticated:
        overview={}
        groups_show=[]
        Groups=content_downloader_groups.objects.filter(user=request.user)
        i=0
        for grp in Groups:
            groups_show.append(grp.name)
            Overview=user_content_downloader.objects.filter(name=grp)
            for over in Overview:
              overview[i]={}
              overview[i]['id']=over.id
              overview[i]['group']=over.name.name
              overview[i]['shop-name']=over.store_name
              overview[i]['image']=over.image
              overview[i]['title']=over.product_name
              overview[i]['price']=over.price
              overview[i]['price_krw']=over.price_krw
              overview[i]['details']=over.details
              overview[i]['url']=over.url
              i+=1

        context={
        'overview':json.dumps(overview),
        'groups':groups_show,
        'section' : 'findProduct'
        }
        return render(request, 'mysite/home.html', context)
    context={
        'section' : 'findProduct'
    }
    return render(request, 'mysite/homebeforeLogin.html' , context)



# Keyword View ...
@login_required
def keyword_view(request):
    if request.user.is_authenticated:
        overview={}
        groups_show=[]
        Groups=keyword_groups.objects.filter(user=request.user)
        i=0
        for grp in Groups:
            groups_show.append(grp.name)
            Overview=user_keywords.objects.filter(name=grp)
            for over in Overview:
              overview[i]={}
              overview[i]['id']=over.id
              overview[i]['group']=over.name.name
              overview[i]['category_name']=over.category_name
              overview[i]['category_id']=over.category_id
              overview[i]['title']=over.product_name
              overview[i]['description']=over.details
              overview[i]['keywords']=over.keywords
              overview[i]['url']=over.url
              i+=1

        context={
        'overview':json.dumps(overview),
        'groups':groups_show,
        'section' : 'keyword_page',
        'section_2' : 'current_keyword'
        }
        return render(request, 'mysite/keyword.html', context)

    context={
        'section' : 'findProduct'
    }
    return render(request, 'mysite/homebeforeLogin.html' , context)

# Login View ...
def login_user(request):
    if request.method!= 'POST':
        form = loginForm()
    else:
        form = loginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'Usename or password may have been entered incorrectly.')
                return redirect('login')
    
    return render(request, 'mysite/login.html', {'form' : form})

# Logout View ...
def logout_user(request):
    logout(request)
    return redirect('home')


# Register View ...
def register_user(request):
    if request.method!='POST':
        form = registerForm()
        form_2 = profileInformForm()
    else:
        form = registerForm(request.POST)
        form_2 = profileInformForm(request.POST)
        if form.is_valid() & form_2.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email']
            user.save()
            profile = profileModel.objects.create(user=user)
            profile.my_store_url = form_2.cleaned_data['my_store_url']
            profile.save()
            current_site = get_current_site(request)
            message = render_to_string('mysite/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'mysite/acc_active_email_confirm.html', {'emailID': to_email})
        else:
            messages.warning(request, 'Invalid form inputs.')
            return redirect('register')
    context={
        'form' : form, 
    }
    return render(request, 'mysite/register.html', context )


# Activate View for registration
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Your account has been activated successfully.')
        return redirect('login')
    else:
        messages.error(request, 'This activation has been expired or invalid.')
        return redirect('register')

# User Profile View
@login_required()
def profile_user(request):
    if request.method!='POST':
        form = EditProfileForm(instance = request.user)
    else:
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been updated.')
            return redirect('home')
    try:
        profile=profileModel.objects.get(user=request.user)
       
    except:
        profile=None
    context={
        'profile' : profile,
        'section' : "settings",
        'form' : form
    }
    return render(request, 'mysite/profile.html',context)


@login_required()
def change_password(request):
    if request.method!='POST':
        form = PasswordChangeForm(user = request.user)
    else:
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password has been updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid form inputs.')
    return render(request, 'mysite/change_password.html' , {'form': form , 'section' : 'settings'})


@login_required
def delete_profileImage(request):
    try:
        profilePicture.objects.get(user=request.user).delete()
        messages.warning(request,'Profile Picture has been removed.')
        return redirect('profile')
    except:
        return redirect('profile')

@login_required
def upload_profileImage(request):
    if request.method == "POST":
        try:
            profile = profilePicture.objects.create(user=request.user)
            profile.profileImage = request.FILES['profileImage']
            profile.save()
            messages.info(request,'Profile Picture has been updated.')
            return redirect('profile')
        except:
            messages.info(request,'Default Profile Picture has been updated.')
            return redirect('profile')
    else:
        return redirect('profile')

def del_user(request):    
    try:
        u = User.objects.get(username = request.user.username)
        u.delete()
        messages.success(request, "The user is deleted")            

    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")    
        return render(request, 'front.html')

    except Exception as e: 
        return redirect('home')

    return redirect('home') 