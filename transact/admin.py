from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Issuer)
admin.site.register(IssuerAccount)
admin.site.register(Offering)
admin.site.register(EscrowAccount)
admin.site.register(Account)
admin.site.register(Entity)
admin.site.register(Party)
admin.site.register(ExternalAccount)
admin.site.register(UploadAccountDocument)
admin.site.register(UploadEntityDocument)
admin.site.register(UploadPartyDocument)
admin.site.register(KYCandAML)
admin.site.register(MyClass)
admin.site.register(Link)