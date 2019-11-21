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

        if request.GET.get('create'):
            keyword_groups(name=request.GET.get('create'),user=request.user).save()

        if request.GET.get('groupdelete'):
            keyword_groups.objects.filter(name=request.GET.get('groupdelete'),user=request.user).delete()

        if request.GET.get('edit'):
            user_keywords.objects.filter(id=request.GET.get('edit')).update(keywords=request.GET.get('new_keywords'))

        return HttpResponse(json.dumps('Success'), content_type='application/json')       

    if request.method == 'POST':
        key=request.POST.get('key')
        company=request.POST.get('company')
        sup=keyword_finder(key,company)        
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
            

            net_profit_min=(t.selling_price_min-t.local_delievery_cost)-total_cost_min-((t.selling_price_min-t.local_delievery_cost)-total_cost_min)*t.vat
            net_profit_max=(t.selling_price_max-t.local_delievery_cost)-total_cost_max-((t.selling_price_max-t.local_delievery_cost)-total_cost_max)*t.vat
            net_profit_avg=(t.selling_price_avg-t.local_delievery_cost)-total_cost_avg-((t.selling_price_avg-t.local_delievery_cost)-total_cost_avg)*t.vat

            profs[key]={}
            profs[key]['Group']="Uncategorized"
            profs[key]['Title']=t.product_name
            profs[key]['china-price']=str(t.china_price_min)+','+str(t.china_price_avg)+','+str(t.china_price_max)
            profs[key]['exchange_rate']=t.exchange_rate
            profs[key]['shipping']=str(t.oversea_shipping)
            profs[key]['extra_cost']=t.extra_cost
            profs[key]['tax_rate']=t.tax_rate
            profs[key]['vat']=t.vat
            profs[key]['total-cost']=str(total_cost_min)+','+str(total_cost_avg)+','+str(total_cost_max)
            profs[key]['selling_price']=str(t.selling_price_min)+','+str(t.selling_price_avg)+','+str(t.selling_price_max)
            profs[key]['local']=t.local_delievery_cost
            profs[key]['consumer_price']=str(t.selling_price_min-t.local_delievery_cost)+','+str(t.selling_price_avg-t.local_delievery_cost)+','+str(t.selling_price_max--t.local_delievery_cost)
            profs[key]['net profit']=str(net_profit_min)+','+str(net_profit_avg)+','+str(net_profit_max)
            profs[key]['id']=t.id
    
            return HttpResponse(json.dumps([create,profs,t.id]), content_type='application/json')

        website=request.POST.get('website')
        file_names=[]
        if 'file[]' in request.FILES:
            file = request.FILES.getlist('file[]')
            for myfile in file:
                if not os.path.exists(settings.MEDIA_ROOT + "\\users" + "\\" + request.user.username+"\\"+myfile.name):
                    fs = FileSystemStorage(settings.MEDIA_ROOT + "\\users" + "\\" + request.user.username)
                    filename = fs.save(myfile.name, myfile)
                file_names.append(settings.MEDIA_ROOT + "\\users" + "\\" + request.user.username+"\\"+myfile.name)
        
        keys=request.POST.getlist('keys[]')
        prof=profitcal(file_names,website,keys)
        profs={}
        try:
            profit_groups.objects.get(user=request.user,name="Uncategorized")
        except profit_groups.DoesNotExist:
            grp=profit_groups(user=request.user,name="Uncategorized")
            grp.save()
        for key in prof.keys(): 
            t=user_profit(china_price_min=prof[key]['min'],china_price_max=prof[key]['max'],product_name=prof[key]['title'],key=prof[key]['key'],name=profit_groups.objects.get(name='Uncategorized',user=request.user)) 
            total_cost_min=(t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate+(t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat+(t.china_price_min*t.exchange_rate+t.extra_cost+t.oversea_shipping)
            total_cost_max=(t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate+(t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat+(t.china_price_max*t.exchange_rate+t.extra_cost+t.oversea_shipping)
            total_cost_avg=(t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.tax_rate+(t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)*t.vat+(t.china_price_avg*t.exchange_rate+t.extra_cost+t.oversea_shipping)
            

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
            profs[key]['shipping']=str(t.oversea_shipping)
            profs[key]['extra_cost']=t.extra_cost
            profs[key]['tax_rate']=t.tax_rate
            profs[key]['vat']=t.vat
            profs[key]['total-cost']=str(total_cost_min)+','+str(total_cost_avg)+','+str(total_cost_max)
            profs[key]['selling_price']=str(t.selling_price_min)+','+str(t.selling_price_avg)+','+str(t.selling_price_max)
            profs[key]['local']=t.local_delievery_cost
            profs[key]['consumer_price']=str(t.selling_price_min-t.local_delievery_cost)+','+str(t.selling_price_avg-t.local_delievery_cost)+','+str(t.selling_price_max--t.local_delievery_cost)
            profs[key]['net profit']=str(net_profit_min)+','+str(net_profit_avg)+','+str(net_profit_max)
            profs[key]['id']=t.id
    
        return HttpResponse(json.dumps(profs), content_type='application/json')
    dir_list = next(os.walk(settings.MEDIA_ROOT))[1]
    try:
        if 'users' not in dir_list:
            os.mkdir(os.path.join(settings.MEDIA_ROOT,settings.MEDIA_ROOT +  '\\users'))
    except:
        pass
    if request.user.is_authenticated:
        try:
            dirname = settings.MEDIA_ROOT + '\\users'
            if request.user.username not in next(os.walk(dirname))[1]:
                os.mkdir(os.path.join(dirname, request.user.username))
        except:
            pass

        dir_list= (next(os.walk(settings.MEDIA_ROOT + "\\users"))[1])
        user_dir_list = dir_list[dir_list.index(request.user.username)]
        user_dir_list= next(os.walk(settings.MEDIA_ROOT + "\\users" + "\\" + user_dir_list))[1]

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
            
                net_profit_min=(over.selling_price_min-over.local_delievery_cost)-total_cost_min-((over.selling_price_min-over.local_delievery_cost)-total_cost_min)*over.vat
                net_profit_max=(over.selling_price_max-over.local_delievery_cost)-total_cost_max-((over.selling_price_max-over.local_delievery_cost)-total_cost_max)*over.vat
                net_profit_avg=(over.selling_price_avg-over.local_delievery_cost)-total_cost_avg-((over.selling_price_avg-over.local_delievery_cost)-total_cost_avg)*over.vat
                
                overview[i]['Group']=over.name.name
                overview[i]['Title']=over.product_name
                overview[i]['china-price']=str(over.china_price_min)+','+str(over.china_price_avg)+','+str(over.china_price_max)
                overview[i]['exchange_rate']=over.exchange_rate
                overview[i]['shipping']=str(over.oversea_shipping)
                overview[i]['extra_cost']=over.extra_cost
                overview[i]['tax_rate']=over.tax_rate
                overview[i]['vat']=over.vat
                overview[i]['total-cost']=str(total_cost_min)+','+str(total_cost_avg)+','+str(total_cost_max)
                overview[i]['selling_price']=str(over.selling_price_min)+','+str(over.selling_price_avg)+','+str(over.selling_price_max)
                overview[i]['local']=over.local_delievery_cost
                overview[i]['consumer_price']=str(over.selling_price_min-over.local_delievery_cost)+','+str(over.selling_price_avg-over.local_delievery_cost)+','+str(over.selling_price_max--over.local_delievery_cost)
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

        if request.GET.get('create'):
            content_downloader_groups(name=request.GET.get('create'),user=request.user).save()

        if request.GET.get('groupdelete'):
            content_downloader_groups.objects.filter(name=request.GET.get('groupdelete'),user=request.user).delete()

        return HttpResponse(json.dumps('Success'), content_type='application/json')       

    if request.method == 'POST':
        Urls=request.POST.getlist('urls[]')
        website=request.POST.get('website')
        cont=content(Urls,website)

        try:
            content_downloader_groups.objects.get(user=request.user,name="Uncategorized")
        except content_downloader_groups.DoesNotExist:
            grp=content_downloader_groups(user=request.user,name="Uncategorized")
            grp.save()
        for key in cont.keys(): 
            t=user_content_downloader(store_name=cont[key]['shop-name'],product_name=cont[key]['title'],price=cont[key]['price'],name=content_downloader_groups.objects.get(name='Uncategorized',user=request.user),details=cont[key]['details'],url=cont[key]['url'],image=cont[key]['image']) 
            t.save()
            cont[key]['id']=t.id

        return HttpResponse(json.dumps(cont), content_type='application/json')

def supplier_find(request):
    if request.method == 'GET':

        if request.GET.get('delete'):
            user_supplier_finder.objects.filter(id=request.GET.get('delete')).delete()

        if request.GET.get('move'):
            user_supplier_finder.objects.filter(id=request.GET.get('move')).update(name=supplier_finder_groups.objects.get(user=request.user,name=request.GET.get('group')))

        if request.GET.get('create'):
            supplier_finder_groups(name=request.GET.get('create'),user=request.user).save()

        if request.GET.get('groupdelete'):
            supplier_finder_groups.objects.filter(name=request.GET.get('groupdelete'),user=request.user).delete()

        return HttpResponse(json.dumps('Success'), content_type='application/json')       

    if request.method == 'POST':
        keys=request.POST.getlist('keys[]')
        website=request.POST.get('website')
        sup=supplier(keys,website)

        try:
            supplier_finder_groups.objects.get(user=request.user,name="Uncategorized")
        except supplier_finder_groups.DoesNotExist:
            grp=supplier_finder_groups(user=request.user,name="Uncategorized")
            grp.save()
        for key in sup.keys(): 
            t=user_supplier_finder(store_name=sup[key]['shop-name'],product_name=sup[key]['title'],price=sup[key]['price'],name=supplier_finder_groups.objects.get(name='Uncategorized',user=request.user),details=sup[key]['region'],url=sup[key]['url']) 
            t.save()
            for img in sup[key]['image']:
                i=supplier_finder_image(src=img,supplier=t)
                i.save()
            sup[key]['id']=t.id
        return HttpResponse(json.dumps(sup), content_type='application/json')

def supplier_finder(request):
    dir_list = next(os.walk(settings.MEDIA_ROOT))[1]
    try:
        if 'users' not in dir_list:
            os.mkdir(os.path.join(settings.MEDIA_ROOT,settings.MEDIA_ROOT +  '\\users'))
    except:
        pass
    if request.user.is_authenticated:
        try:
            dirname = settings.MEDIA_ROOT + '\\users'
            if request.user.username not in next(os.walk(dirname))[1]:
                os.mkdir(os.path.join(dirname, request.user.username))
        except:
            pass
        dir_list= (next(os.walk(settings.MEDIA_ROOT + "\\users"))[1])
        user_dir_list = dir_list[dir_list.index(request.user.username)]
        user_dir_list= next(os.walk(settings.MEDIA_ROOT + "\\users" + "\\" + user_dir_list))[1]
        overview={}
        groups_show=[]
        Groups=supplier_finder_groups.objects.filter(user=request.user)
        i=0
        for grp in Groups:
            if grp.name!="Uncategorized":
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
              overview[i]['details']=over.details
              overview[i]['url']=over.url
              i+=1

        context={
        'overview':json.dumps(overview),
        'groups':groups_show,
            'section' : 'findProduct',
            'user_directories' : user_dir_list
        }
        return render(request, 'mysite/supplier_finder.html', context)
    context={
        'section' : 'findProduct'
    }
    return render(request, 'mysite/homebeforeLogin.html' , context)
# Home View (Product Tracker) ...
def home(request):

        overview={}
        groups_show=[]
        Groups=content_downloader_groups.objects.filter(user=request.user)
        i=0
        for grp in Groups:
            if grp.name!="Uncategorized":
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
              overview[i]['details']=over.details
              overview[i]['url']=over.url
              i+=1

        context={
        'overview':json.dumps(overview),
        'groups':groups_show,
            'section' : 'findProduct',
        }
        return render(request, 'mysite/home.html', context)
    context={
        'section' : 'findProduct'
    }
    return render(request, 'mysite/homebeforeLogin.html' , context)



# Keyword View ...
@login_required
def keyword_view(request):
    dir_list = next(os.walk(settings.MEDIA_ROOT))[1]
    try:
        if 'users' not in dir_list:
            os.mkdir(os.path.join(settings.MEDIA_ROOT,settings.MEDIA_ROOT +  '\\users'))
    except:
        pass
    if request.user.is_authenticated:
        try:
            dirname = settings.MEDIA_ROOT + '\\users'
            if request.user.username not in next(os.walk(dirname))[1]:
                os.mkdir(os.path.join(dirname, request.user.username))
        except:
            pass
        dir_list= (next(os.walk(settings.MEDIA_ROOT + "\\users"))[1])
        user_dir_list = dir_list[dir_list.index(request.user.username)]
        user_dir_list= next(os.walk(settings.MEDIA_ROOT + "\\users" + "\\" + user_dir_list))[1]
        overview={}
        groups_show=[]
        Groups=keyword_groups.objects.filter(user=request.user)
        i=0
        for grp in Groups:
            if grp.name!="Uncategorized":
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
    else:
        form = registerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email']
            user.save()
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
    if request.method!="POST":
        form = EditProfileForm(instance = request.user)
    else:
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been updated')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid form inputs.')
    context={
        'section' : 'settings'
    }
    return render(request, 'mysite/profile.html', context )


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
