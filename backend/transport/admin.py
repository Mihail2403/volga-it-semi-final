from django.contrib import admin

from transport.models import Transport, TransportType

# Register your models here.
admin.site.register(Transport)
admin.site.register(TransportType)