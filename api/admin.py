from django.contrib import admin

from .models import authTokens, links

# Register your models here.

admin.site.register(links)
admin.site.register(authTokens)