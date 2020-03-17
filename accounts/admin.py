from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Activation)
admin.site.register(StripeUserID)
# admin.site.register(User)



