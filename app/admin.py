from django.contrib import admin
from app.models import *

admin.site.register(Client)
admin.site.register(Subscription)
admin.site.register(SecretKey)
admin.site.register(WebsiteKey)
admin.site.register(AccountContact)
