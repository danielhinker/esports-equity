from django import forms
from .models import *
from django.views import generic

# class CustomerCreateForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields =['address_1','address_2','city','country',
#                  'zip','card_number','cvc','exp_month','exp_year','card_type']
#
# class ChargeCreateForm(forms.ModelForm):
#     class Meta:
#         model = Backings
#         fields = ('amount',)
#         labels = {'email': 'How much money would you like to back?'}
#
class ChargeCreateForm(forms.ModelForm):
    class Meta:
        model = Charge
        fields = ('balance_transaction',)


class ChargeCreateForm2(forms.Form):
    amount = forms.IntegerField()

        # token = self.request.POST['stripeToken']