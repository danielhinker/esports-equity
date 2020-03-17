from django import forms

from django.shortcuts import render, get_object_or_404
from accounts.models import User

from .models import *


class MyForm(forms.ModelForm):
    class Meta:
        model = MyClass
        fields = '__all__'


class AccountCreateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['accountRegistration', 'type', 'entityType', 'domesticYN', 'streetAddress1', 'city', 'state',
                  'zip', 'country', 'KYCstatus', 'AMLstatus', 'AccreditedStatus', 'approvalStatus']


# class AccountCreateForm1(forms.ModelForm):
#     class Meta:
#         model = Issuer
#         fields = ['email', 'firstName', 'lastName', 'issuerName']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['firstName'].label = "First Name"
    #     self.fields['lastName'].label = "Last Name"
    #     self.fields['issuerName'].label = "Issuer Name"
    #     self.fields['email'].label = "Email"


class IssuerCreateForm(forms.ModelForm):
    class Meta:
        model = Issuer
        fields = ['email', 'firstName', 'lastName', 'issuerName']
        help_texts = {
            'email': 'Email of issuer',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['firstName'].label = "First Name"
        self.fields['lastName'].label = "Last Name"
        self.fields['issuerName'].label = "Issuer Name"
        self.fields['email'].label = "Email"


class IssuerAccountCreateForm(forms.ModelForm):
    class Meta:
        model = IssuerAccount
        fields = ['companyName', 'companyState', 'issuingCountry']


class PartyCreateForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ['domicile', 'firstName', 'lastName', 'dob', 'primCountry', 'primAddress1',
                  'primCity', 'primState', 'primZip', 'emailAddress', 'socialSecurityNumber']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['firstName'].label = "First Name"
    #     self.fields['lastName'].label = "Last Name"
    #     self.fields['middleInitial'].label = "Middle Initial"
        # self.fields['email'].label = "Email"
#


class UpdateParty(forms.ModelForm):

    class Meta:
        model = Party
        exclude = ('partyId', 'createdIpAddress')


class EntityCreateForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = ['domicile', 'entityName', 'primCountry', 'primAddress1',
                  'primCity', 'primState', 'primZip', 'emailAddress']


class OfferingCreateForm(forms.ModelForm):

    class Meta:
        model = Offering
        exclude = ('issuer', 'offeringId', 'offeringStatus', 'createdIPAddress', 'issuerId')


class ExternalAccountCreateForm(forms.ModelForm):
    class Meta:
        model = ExternalAccount
        exclude = ('user', 'accountId', 'updatedIpAddress', 'statusCode', 'statusDesc')


# class CreateLink(forms.ModelForm):
#     class Meta:
#         model = Link


class EscrowAccountCreateForm(forms.ModelForm):
    class Meta:
        model = EscrowAccount
        exclude = ('issuerId', 'escrowAccountStatus')


class CalculateSuitabilityForm(forms.ModelForm):
    class Meta:
        model = Suitability
        exclude = ('account', 'accountId',)


class PerformKYCandAMLCreateForm(forms.ModelForm):
    class Meta:
        model = KYCandAML
        fields = []

class UpdateKYCandAMLCreateForm(forms.ModelForm):
    class Meta:
        model = KYCandAML
        fields = ['partyId', 'idNumber', 'qns1', 'qns2',
                  'qns3', 'qns4', 'qns5']

class LinkCreateForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ('linkId', 'firstEntry', 'firstEntryType', 'relatedEntryType', 'relatedEntry', 'linkType')


class UploadAccountDocumentForm(forms.ModelForm):
    class Meta:
        model = UploadAccountDocument
        exclude = ('document_details',)


class UploadPartyDocumentForm(forms.ModelForm):
    class Meta:
        model = UploadPartyDocument
        exclude = ('document_details',)


class UploadEntityDocumentForm(forms.ModelForm):
    class Meta:
        model = UploadEntityDocument
        exclude = ('document_details',)


class TradeCreateForm(forms.ModelForm):
    class Meta:
        model = Trade
        exclude = ('partyId', 'tradeId', 'transactionId', 'transactionAmount',
                   'transactionDate', 'transactionStatus', 'TradeFinancialDetails',
                   'orderStatus', 'createdIpAddress', 'funds')




# class UpdateKycAml(forms.ModelForm):
#     class Meta:
#         model = KYCandAML
#         exclude = ('partyId', 'noOfqns', 'idNumber' 'kycStatus')
# class User(forms.ModelForm):
#     class Meta:
#         model = User

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['clientID'].label = "Client ID"
    #     self.fields['developerAPIKey'].label = "Developer API Key"

# class Issuer(forms.ModelForm):
#     class Meta:
#         model = Issuer


# class PersonalInformationCreateForm(forms.ModelForm):
#     class Meta:
#         model = Party
#         fields = ('invest_to', 'firstName', 'lastName', 'primAddress1', 'primAddress2',
#                    'primCity', 'primState', 'primZip', 'primCountry',)
#
# class BackgroundInformationCreateForm(forms.ModelForm):
#     class Meta:
#         model = Party
#         fields = ('empName', 'occupation', 'empAddress1', 'empAddress2',
#                    'empCity', 'empState', 'empZip', 'empCountry', 'associatedPerson', 'assets')
#
# class PersonalVerificationCreateForm(forms.ModelForm):
#     class Meta:
#         model = Party
#         fields = ('primCountry', 'socialSecurityNumber')
#
# class FollowUpQuestions(forms.ModelForm):
#     class Meta:
#         model = Party
#         fields = ('')
#
# class UploadVerificationDocuments:
#     class Meta:
#         model = Party
#         fields = ('identificationNumber', 'socialSecurityNumber' 'uploadDocuments')
#
# class YourFinancialInformation:
#     class Meta:
#         model = Party
#         fields = ('AccreditedStatus', 'socialSecurityNumber' 'uploadDocuments')
#
# class FundingMethod:
#     pass
