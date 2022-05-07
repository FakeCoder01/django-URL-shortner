import datetime, json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from api.models import links, authTokens
from django.core.validators import URLValidator
from django.utils.crypto import get_random_string
import random
# Create your views here.


def regAPI(request):
    if request.method == 'POST':
        api_key = request.POST['api_key']
        email = request.POST['email']

        if isLoggedin(request):
            if authTokens.objects.filter(email=email, api_key=api_key, status='Active').exists():
                r_api_key = get_random_string(10)
                authTokens.objects.filter(email=email, api_key=api_key).update(api_key=r_api_key)
                request.session['user'] = {'api_key' : r_api_key }
                return JsonResponse(json.dumps({'api_key': r_api_key, 'msg' : 'API_KEY Updated'}), content_type="application/json", safe=False) 
            else:
                return redirect('/')
        else:
            return redirect('/')     
            
    else:
        return redirect('/')            









def isLoggedin(request):
    try:
        if(request.session['user'].get('isLoggedin') == True and request.session['user'].get('email') != None and request.session['user'].get('api_key') != None):
            return True
        else:
            return False            
    except:
            return False      
def shoot_out(request, lid):
    try:
        if links.objects.filter(lid=lid).exists():
            qs = links.objects.filter(lid=lid).first()
            r_url = qs.link
            validate = URLValidator()
            try: 
                validate(qs.link)
                return redirect(r_url)
            except:
                return redirect('http://'+ qs.link)
        else:
            return render(request, 'wrong-url.html')
    except:
         return render(request, 'wrong-url.html')       
     
def index(request):
    return render(request, 'home.html')


def account(request):
    if isLoggedin(request):
        if request.session['user'].get('status') == 'Active':
            return render(request, 'acc.html', {'context':request.session['user']})
        else:
            return render(request, 'login.html', {'context':request.session['user'], 'div': 'otp'})        

    elif request.method == 'POST':
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        if authTokens.objects.filter(email=email, psw=psw).exists():
            qs = authTokens.objects.filter(email=email, psw=psw).first()
            request.session['user'] = {
                'isLoggedin' : True,
                'api_key': qs.api_key,
                'email' : qs.email,
                'status': qs.status
            }
            if qs.status == 'Active':
                return render(request, 'acc.html', {'context': request.session['user']})
            else:
                return render(request, 'login.html', {'context':request.session['user'], 'div': 'otp'})    
        elif authTokens.objects.filter(email=email).exists():
            return render(request, 'login.html', {'context': 'Wrong password. <a href="/acc/reset-psw/">reset password<a/>'})
        else:
            otp = random.randint(100000,999999)
            api_key = get_random_string(10)
            created_on = datetime.datetime.now()
            su = authTokens(email=email, psw=psw, otp=otp, api_key=api_key, status='Inactive', created_on=created_on)
            su.save()
            request.session['user'] = {
                'isLoggedin' : True,
                'api_key': api_key,
                'email' : email,
                'status': 'Inactive'
            }
            return render(request, 'login.html', {'context':request.session['user'], 'div': 'otp'})
    else:
        return render(request, 'login.html')    


def otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        if authTokens.objects.filter(email=email, otp=otp).exists():
            qs = authTokens.objects.filter(email=email, otp=otp).first()
            r_otp = random.randint(100000,999999)
            authTokens.objects.filter(email=email, otp=otp).update(otp=r_otp)
            authTokens.objects.filter(email=email, otp=r_otp).update(status='Active')
            request.session['user'] = {
                'isLoggedin' : True,
                'api_key': qs.api_key,
                'email' : qs.email,
                'status': qs.status
            }
            return render(request, 'acc.html', {'context': request.session['user']})
        else:
            return render(request, 'login.html', {'context':request.session['user'], 'div': 'otp', 'msg' : 'Wrong otp'})
    else:
        return redirect('/')
        
def logout(request):
    try:
        del request.session['user']
        return redirect('/acc/user')
    except:
        return redirect('/acc/user')

