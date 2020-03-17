from rest_framework import serializers
from .models import *


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
       
        fields = ('accountId',)


class IssuerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issuer
   
        fields = ('issuerId', 'issuerStatus')


class PartyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
   
        fields = ('partyId',)


class EntityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        
        fields = ('partyId',)



class OfferingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offering

        fields = ('offeringId', 'offeringStatus')


class EscrowAccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscrowAccount
       
        fields = ('issuerId', 'escrowAccountStatus')


class PerformKYCandAMLPartyCreateSerializer(serializers.ModelSerializer):
    class Meta:
            model = KYCandAML
            exclude = ('partyId', 'qns1', 'qns2', 'qns3', 'qns4', 'qns5',
                       'kycStatus', 'AML', 'party')


class UpdateKYCandAMLPartyCreateSerializer(serializers.ModelSerializer):
    class Meta:
            model = KYCandAML
            fields = ('partyId', 'kycStatus')

class LinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('linkId',)


class UploadAccountDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadAccountDocument
        fields = ('document_details',)


class TradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ('tradeId', 'transactionId', 'transactionAmount',
                   'transactionDate', 'transactionStatus',)