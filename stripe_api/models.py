from django.db import models
# from django.forms import extras
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from django.conf import settings
from .choices import *

from accounts.models import User
from teams.models import Team
from django.utils import timezone

#
# class Customer(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer')
#     stripe_id = models.CharField(max_length=255)
#     address_1 = models.CharField(max_length=128, default=None)
#     address_2 = models.CharField(max_length=128, default=None, blank=True)
#     city = models.CharField(max_length=64, default=None)
#     country = models.CharField(choices=COUNTRIES, max_length=2, default='US')
#     zip = models.CharField(max_length=5, default=None)
#     card_number = models.CharField(max_length=16, default=None)
#     cvc = models.CharField(max_length=3, default=None)
#     exp_month = models.CharField(choices=MONTHS, max_length=2, default='01')
#     exp_year = models.CharField(max_length=4, default=None)
#     card_type = models.CharField(choices=CARD_TYPE, max_length=6, default='Credit')


# class BackedCustomers(models.Model):
#     backed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='backed_by')
#     date_backed = models.DateField(auto_now_add=True)
#     backed_team = models.ForeignKey(Team, null=True, blank=False)
#     backed_amount = models.IntegerField(blank=True, default=0)


# class Backings(models.Model):
#     user = models.ForeignKey(User, related_name='backed_by')
#     team = models.ForeignKey(Team, related_name='teams_backed')
#     amount = models.DecimalField(max_digits=6, decimal_places=2)
#     # date_backed = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return str(self.amount)

#
class Charge(models.Model):
    # user = models.ForeignKey(User, related_name='backings', blank=True, null=True)
    # team = models.ForeignKey(Team, related_name='backed_by', blank=True, null=True)
    balance_transaction = models.IntegerField(blank=True, null=True)
    charge_id = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    date_backed = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.balance_transaction)



