from django.contrib import admin
from .models import Flight, Medical, AccountDetail, CertificatesHeld, RatingsHeld

# Register your models here.
admin.site.register(Flight)
admin.site.register(Medical)
admin.site.register(AccountDetail)
admin.site.register(CertificatesHeld)
admin.site.register(RatingsHeld)