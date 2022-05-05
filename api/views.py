import json
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import links
from django.utils.crypto import get_random_string
import  datetime

# Create your views here.

def shorten_url(link):
    if links.objects.filter(link=link).exists():
        qs = links.objects.filter(link=link).first()
        return qs.lid
    else: 
        lid = get_random_string(6)
        while links.objects.filter(lid=lid).exists():
            lid = get_random_string(6)
        created_on = datetime.datetime.now()
        save_link = links(lid=lid, link=link, created_on=created_on)
        save_link.save()
        return lid

def short(request):
    if request.method == 'POST':
        lid = shorten_url(request.POST.get('link'))
        return JsonResponse(json.dumps({'surl': lid,}), content_type="application/json", safe=False) 
    else:
        return redirect('/?e=PR') 