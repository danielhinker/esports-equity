from rest_framework import serializers
from .models import *
from accounts.models import *
#
# class CustomerCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = '__all__'
#         # fields = ('accountId',)


# class ChargeCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Charge
#         fields = ('charge_id',)
#         # fields = ('accountId',)


class StripeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeUserID
        fields = ('stripe_user_id',)