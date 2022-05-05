from django.shortcuts import redirect, render
from api.models import links
from django.core.validators import URLValidator
# Create your views here.


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