import json
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import links
from django.utils.crypto import get_random_string
import  datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import LinkSerializers
from .models import links, authTokens

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


class URL_SHORTNER(APIView):
    
    def get(self, request, *args, **kwargs):

        try:
            api_key = request.GET['api_key']
            link = request.GET['link']
        except:
            return Response({'error' : 'feilds not set'})
     
        if authTokens.objects.filter(api_key=api_key).exists():

            if links.objects.filter(link=link).exists():
                qs = links.objects.filter(link=link).first()
                data = {
                    'lid': qs.lid,
                    'link': link,
                    'trough': qs.trough,
                    'api_key' : api_key,
                    'created_on' : qs.created_on
                }
                return Response(data)
            else:
                lid = get_random_string(6)
                while links.objects.filter(lid=lid).exists():
                    lid = get_random_string(6)
                data = {
                    'lid': lid,
                    'link': link,
                    'trough': 'api',
                    'api_key' : api_key,
                    'created_on' : datetime.datetime.now()
                }
                serializer = LinkSerializers(data=data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors)
        else:
            return Response({'error':'wrong api_key'}) 



