from django.contrib import admin

from .models import Prize, OwnPrize, CheckIn

admin.site.register(Prize)
admin.site.register(OwnPrize)
admin.site.register(CheckIn)
