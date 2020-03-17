from django.shortcuts import render, get_object_or_404
from django.views.generic import (

    CreateView, UpdateView, DeleteView
)

from django.urls import reverse_lazy
import requests
from django.http import HttpResponseRedirect
from .forms import *
from .serializer import *
from .models import *
from eeweb.settings import APIKEY
from accounts.models import User


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class MyView(CreateView):
    form_class = MyForm
    template_name = "transact/account_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.createdIpAddress = get_client_ip(self.request)
        return super().form_valid(form)


class AccountCreateView(CreateView):
    form_class = AccountCreateForm
    template_name = "transact/account_create.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)


    def form_valid(self, form):
        form.instance.user = self.request.user
        form_object = form.save()
        form_data = form.cleaned_data
        form_data.update(**APIKEY)
        r = requests.put('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/createAccount',
                         data=form_data)
        json = r.json()
        json_dict = dict(json['accountDetails'][0].items())
        del json['accountDetails']
        json.update(**json_dict)
        serializer = AccountCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
            return super().form_valid(form)


class AccountUpdateView(UpdateView):
    form_class = AccountCreateForm
  
    template_name = 'transact/account_update.html'
    success_url = reverse_lazy("accounts:profile_settings")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        account_object = user_object.account.get(user__pk=user_object.pk)
        
        return account_object

    def form_valid(self, form):
        
        form.instance.updatedIpAddress = get_client_ip(self.request)
        form_object = form.save()
      
        form_data = {}
        form_data.update(**form_object.__dict__)
        form_data.update(**APIKEY)
        r = requests.put('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/updateAccount',
                          data=form_data)
        json = r.json()
        json_dict = dict(json['accountDetails'][0].items())
        del json['accountDetails']
        json.update(**json_dict)
        serializer = AccountCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return HttpResponseRedirect(self.get_success_url())


class AccountDeleteView(DeleteView):
    model = Issuer
    template_name = 'transact/issuer_delete.html'
    success_url = reverse_lazy("accounts:profile_settings")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        account_object = user_object.account.get(user__pk=user_object.pk)
        """ Hook to ensure object is owned by request.user. """
        return account_object

    def delete(self, *args, **kwargs):
        form_data = self.get_object().__dict__
        form_data.update(**APIKEY)
        requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/deleteAccount',
                      data=form_data)
        super().delete(*args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


class IssuerCreateView(CreateView):
    form_class = IssuerCreateForm
    template_name = "transact/issuer_create.html"
    success_url = reverse_lazy("accounts:profile_settings")

    def get_initial(self):
        user = get_object_or_404(User, pk=self.request.user.pk)
        return {
            'email': user.email,
            'firstName': user.first_name,
            'lastName': user.last_name,
        }

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.createdIpAddress = get_client_ip(self.request)
        form_object = form.save()
        form_data = form.cleaned_data
        form_data.update(**APIKEY)
        r = requests.put('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/createIssuer',
                         data=form_data)
        json = r.json()
        json_dict = dict(json['issuerDetails'][1][0].items())
        del json['issuerDetails']
        json.update(**json_dict)
        serializer = IssuerCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return super().form_valid(form)


class IssuerUpdateView(UpdateView):
    form_class = IssuerCreateForm
 
    template_name = 'transact/issuer_create.html'
    success_url = reverse_lazy("accounts:profile_settings")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        issuer_object = user_object.issuer.get(user__pk=user_object.pk)
      
        return issuer_object

    def form_valid(self, form):
        form_object = form.save()
        form_data = form_object.__dict__
        form_data.update(**APIKEY)
        r = requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/updateIssuer',
                          data=form_data)
        json = r.json()
        json_dict = dict(json['issuerDetails'][1][0].items())
        del json['issuerDetails']
        json.update(**json_dict)
        serializer = IssuerCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return HttpResponseRedirect(self.get_success_url())


class IssuerDeleteView(DeleteView):
    model = Issuer
    template_name = 'transact/issuer_delete.html'
    success_url = reverse_lazy("accounts:profile_settings")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        issuer_object = user_object.issuer.get(user__pk=user_object.pk)
        """ Hook to ensure object is owned by request.user. """
        return issuer_object

    def delete(self, *args, **kwargs):
        form_data = self.get_object().__dict__
        form_data.update(**APIKEY)
        requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/deleteIssuer',
                      data=form_data)
        super().delete(*args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())

  
class IssuerAccountCreateView(CreateView):
    form_class = IssuerAccountCreateForm
    template_name = 'transact/issuer_account_create.html'
    success_url = reverse_lazy("accounts:profile_settings")

    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.request.user.pk)
        issuer_object = user.issuer.get(user__pk=user.pk)
        form.instance.issuer = issuer_object
        form.instance.createdIpAddress = get_client_ip(self.request)
        form.instance.issuerId = issuer_object.issuerId
        form_object = form.save()
        form_data = form.cleaned_data
        form_data.update(**issuer_object.__dict__)
        form_data.update(**APIKEY)
        r = requests.put('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/createIssuerAccount',
                         data=form_data)
        return super().form_valid(form)


class IssuerAccountDeleteView(DeleteView):
    model = IssuerAccount
    template_name = 'transact/issuer_account_delete.html'
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        issuer_object = user_object.issuer.get(user__pk=self.request.user.pk)
        issuer_account_object = issuer_object.issuer_account.get(issuer__issuerId=issuer_object.issuerId)
        return issuer_account_object

    def delete(self, *args, **kwargs):
        form_data = self.get_object().__dict__
        form_data.update(**APIKEY)
        requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/deleteIssuerAccount',
                      data=form_data)
        super().delete(*args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


class PartyCreateView(CreateView):
    form_class = PartyCreateForm
    template_name = 'transact/party_create.html'
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        
        form.instance.user = self.request.user
        form_object = form.save()
        form_data = form.cleaned_data
        form_data.update(**APIKEY)
        r = requests.put('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/createParty',
                         data=form_data)
        json = r.json()
        json_dict = json['partyDetails'][1][0]['partyId']
        del json['partyDetails']
        json['partyId'] = json_dict
        serializer = PartyCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return super().form_valid(form)


class PartyUpdateView(UpdateView):
    form_class = UpdateParty
    
    template_name = 'transact/party_update.html'
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        party_object = user_object.party.get(user__pk=user_object.pk)
        
        return party_object

    def form_valid(self, form):
        form_object = form.save()
        form_data = form_object.__dict__
        form_data.update(**APIKEY)
        r = requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/updateParty',
                          data=form_data)
        json = r.json()
        json_dict = dict(json['partyDetails'][1][0].items())
        del json['partyDetails']
        json.update(**json_dict)
        serializer = PartyCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return HttpResponseRedirect(self.get_success_url())


class PartyDeleteView(DeleteView):
    model = Party
    template_name = 'transact/party_delete.html'
    success_url = reverse_lazy("accounts:profile_settings")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        party_object = user_object.party.get(user__pk=user_object.pk)
        """ Hook to ensure object is owned by request.user. """
        return party_object

    def delete(self, *args, **kwargs):
        form_data = self.get_object().__dict__
        form_data.update(**APIKEY)
        requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/deleteParty',
                      data=form_data)
        super().delete(*args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


class EntityCreateView(CreateView):
    form_class = EntityCreateForm
    template_name = "transact/entity_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.createdIpAddress = get_client_ip(self.request)
        form_object = form.save()
        form_data = form.cleaned_data
        form_data.update(**APIKEY)
        r = requests.put('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/createEntity',
                         data=form_data)
        json = r.json()
        json_dict = dict(json['entityDetails'][1][0].items())
        del json['entityDetails']
        json.update(**json_dict)
        serializer = EntityCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return super().form_valid(form)


class EntityUpdateView(UpdateView):
    form_class = EntityCreateForm
    template_name = 'transact/entity_update.html'
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        entity_object = user_object.entity.get(user__pk=user_object.pk)
        return entity_object

    def form_valid(self, form):
        form_object = form.save()
        form_data = form_object.__dict__
        form_data.update(**APIKEY)
        r = requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/updateEntity',
                          data=form_data)
        json = r.json()
        json_dict = dict(json['entityDetails'][1][0].items())
        del json['entityDetails']
        json.update(**json_dict)
        serializer = EntityCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return HttpResponseRedirect(self.get_success_url())


class EntityDeleteView(DeleteView):
    model = Entity
    template_name = 'transact/entity_delete.html'
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        entity_object = user_object.entity.get(user__pk=user_object.pk)
        return entity_object

    def delete(self, *args, **kwargs):
        form_data = self.get_object().__dict__
        form_data.update(**APIKEY)
        requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/deleteEntity',
                      data=form_data)
        super().delete(*args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


class OfferingCreateView(CreateView):
    form_class = OfferingCreateForm
    template_name = "transact/offering_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.request.user.pk)
        issuer_object = user.issuer.get(user__pk=user.pk)
        form.instance.issuer = issuer_object
        form.instance.createdIpAddress = get_client_ip(self.request)
        form.instance.issuerId = issuer_object.issuerId
        form_object = form.save()
        form_data = form_object.__dict__
        form_data.update(**APIKEY)
        form_data.update(**issuer_object.__dict__)
        r = requests.put('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/createOffering',
                         data=form_data)
        json = r.json()
        json_dict = dict(json['offeringDetails'][1][0].items())
        del json['offeringDetails']
        json.update(**json_dict)
        serializer = OfferingCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return super().form_valid(form)


class OfferingUpdateView(UpdateView):
    form_class = OfferingCreateForm
    template_name = 'transact/offering_update.html'
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        issuer_object = user_object.issuer.get(user__pk=user_object.pk)
        offering_object = issuer_object.offering.get(issuer__user__pk=user_object.pk)
        return offering_object

    def form_valid(self, form):
        form_object = form.save()
        form_data = form_object.__dict__
        form_data.update(**APIKEY)
        r = requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/updateOffering',
                          data=form_data)
        json = r.json()
        json_dict = dict(json['offeringDetails'][1][0].items())
        del json['offeringDetails']
        json.update(**json_dict)
        serializer = OfferingCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return HttpResponseRedirect(self.get_success_url())


class OfferingDeleteView(DeleteView):
    model = Offering
    template_name = 'transact/offering_delete.html'
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        issuer_object = user_object.issuer.get(user__pk=user_object.pk)
        offering_object = issuer_object.offering.get(issuer__user__pk=user_object.pk)
        return offering_object

    def delete(self, *args, **kwargs):
        form_data = self.get_object().__dict__
        form_data.update(**APIKEY)
        requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/deleteOffering',
                      data=form_data)
        super().delete(*args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


class ExternalAccountCreateView(CreateView):
    form_class = ExternalAccountCreateForm
    template_name = "transact/external_account_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.updatedIpAddress = get_client_ip(self.request)
        form.save()
        form_data = form.cleaned_data
        form_data.update(**APIKEY)
        requests.put('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/createExternalAccount',
                     data=form_data)
       
        return super().form_valid(form)


class ExternalAccountUpdateView(UpdateView):
    form_class = ExternalAccountCreateForm
    template_name = 'transact/external_account_update.html'
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        external_account_object = user_object.account.get(user__pk=user_object.pk)
        return external_account_object

    def form_valid(self, form):
        form_object = form.save()
        form_data = form_object.__dict__
        form_data.update(**APIKEY)
        requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/updateExternalAccount',
                      data=form_data)
        # json = r.json()
        # json_dict = dict(json['accountDetails'][1][0].items())
        # del json['entityDetails']
        # json.update(**json_dict)
        # serializer = EntityCreateSerializer(data=json)
        # if serializer.is_valid():
        #     serializer.update(instance=self.object, validated_data=serializer.validated_data)
        return HttpResponseRedirect(self.get_success_url())


class ExternalAccountDeleteView(DeleteView):
    model = ExternalAccount
    template_name = 'transact/external_account_delete.html'
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        external_account_object = user_object.account.get(user__pk=user_object.pk)
        return external_account_object

    def delete(self, *args, **kwargs):
        form_data = self.get_object().__dict__
        form_data.update(**APIKEY)
        requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/deleteExternalAccount',
                      data=form_data)
        super().delete(*args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())


class EscrowAccountCreateView(CreateView):
    form_class = EscrowAccountCreateForm
    template_name = "index.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form_object = form.save()
        form_data = form.cleaned_data
        form_data.update(**APIKEY)
        r = requests.put('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/createEntity',
                         data=form_data)
        json = r.json()
        json_dict = dict(json['Financial Escrow Details']['1'][0].items())
        del json['partyId']
        json.update(**json_dict)
        serializer = IssuerCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return super().form_valid(form)


class EscrowAccountUpdateView(UpdateView):
    form_class = EscrowAccountCreateForm
    # form_class = forms.ChangeSettings
    template_name = 'index.html'
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        escrow_account_object = EscrowAccount.objects.get(pk=self.kwargs.get('pk'))
        # escrow_account_object = user_
        return escrow_account_object

    def form_valid(self, form):
        form_object = form.save()
        form_data = form_object.__dict__
        form_data.update(**APIKEY)
        r = requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/updateEscrowAccount',
                          data=form_data)
        json = r.json()
        json_dict = dict(json['ESCROW_DETAILS'][1][0].items())
        del json['ESCROWDETAILS']
        json.update(**json_dict)
        serializer = EscrowAccountCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return HttpResponseRedirect(self.get_success_url())


class EscrowAccountDeleteView(DeleteView):
    model = EscrowAccount
    template_name = 'delete_view.html'
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        escrow_account_object = EscrowAccount.objects.get(pk=self.kwargs.get('pk'))
        # object = form.save()
        form_data = escrow_account_object.__dict__
        form_data.update(**APIKEY)
        requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/deleteEscrowAccount',
                      data=form_data)
        return escrow_account_object


class SuitabilityCalculate(CreateView):
    form_class = CalculateSuitabilityForm
    template_name = 'transact/calculate_suitability.html'
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        account_object = user_object.account.get(user__pk=user_object.pk)
        form.instance.account = account_object
        form_object = form.save()
        form_data = form.cleaned_data
        form_data.update(**APIKEY)
        form_data['accountId'] = account_object.accountId
        r = requests.put('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/calculateSuitability',
                         data=form_data)
        # json = r.json()
        # json_dict = json['partyDetails'][1][0]['partyId']
        # del json['partyDetails']
        # json['partyId'] = json_dict
        # serializer = PartyCreateSerializer(data=json)
        # if serializer.is_valid():
        #     serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return super().form_valid(form)


class SuitabilityUpdate(UpdateView):
    form_class = CalculateSuitabilityForm
    template_name = 'transact/calculate_suitability.html'
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        account_object = user_object.account.get(user__pk=user_object.pk)
        form.instance.account = account_object
        form_object = form.save()
        form_data = form.cleaned_data
        form_data.update(**APIKEY)
        form_data['accountId'] = account_object.accountId
        r = requests.put('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/updateSuitability',
                         data=form_data)
       
        return HttpResponseRedirect(self.get_success_url())


class PerformKYCandAMLParty(CreateView):
    form_class = PerformKYCandAMLCreateForm
    template_name = 'transact/perform_kyc_and_aml.html'
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        party_object = user_object.party.get(user__pk=self.request.user.pk)
        form.instance.party = party_object
        form.instance.partyId = party_object.partyId
        form_object = form.save()
        form_data = form.cleaned_data
        form_data['partyId'] = party_object.partyId
        form_data.update(**APIKEY)
        form_data.update(**party_object.__dict__)
        r = requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/performKycAml',
                         data=form_data)
        json = r.json()

        json['idNumber'] = json['kyc']['response']['id-number']

        json['noOfqns'] = '5'

        json['prompt1'] = json['kyc']['response']['questions']['question'][0]['prompt']
        json['type1'] = json['kyc']['response']['questions']['question'][0]['type']
        json['answer1'] = str(json['kyc']['response']['questions']['question'][0]['answer'])

        json['prompt2'] = json['kyc']['response']['questions']['question'][1]['prompt']
        json['type2'] = json['kyc']['response']['questions']['question'][1]['type']
        json['answer2'] = str(json['kyc']['response']['questions']['question'][1]['answer'])

        json['prompt3'] = json['kyc']['response']['questions']['question'][2]['prompt']
        json['type3'] = json['kyc']['response']['questions']['question'][2]['type']
        json['answer3'] = str(json['kyc']['response']['questions']['question'][2]['answer'])

        json['prompt4'] = json['kyc']['response']['questions']['question'][3]['prompt']
        json['type4'] = json['kyc']['response']['questions']['question'][3]['type']
        json['answer4'] = str(json['kyc']['response']['questions']['question'][3]['answer'])

        json['prompt5'] = json['kyc']['response']['questions']['question'][4]['prompt']
        json['type5'] = json['kyc']['response']['questions']['question'][4]['type']
        json['answer5'] = str(json['kyc']['response']['questions']['question'][4]['answer'])


        del json['kyc']

        serializer = PerformKYCandAMLPartyCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return super().form_valid(form)

Issue_Type = (
    (u'1', u'Equity'),
    (u'2', u'Debt'),
    (u'3', u'Hybrid'),
    (u'4', u'Fund'),
)

class UpdateKYCandAMLParty(UpdateView):
    form_class = UpdateKYCandAMLCreateForm
    template_name = 'transact/update_kyc_and_aml.html'
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        party_object = user_object.party.get(user__pk=user_object.pk)
        kycandaml_object = party_object.KYCandAML.get(party__user__pk=user_object.pk)
        return kycandaml_object

    def form_valid(self, form):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        party_object = user_object.party.get(user__pk=user_object.pk)
        kycandaml_object = party_object.KYCandAML.get(party__user__pk=user_object.pk)
        form.instance.idNumber = kycandaml_object.idNumber
        form.instance.type1 = kycandaml_object.type1
        form.instance.type2 = kycandaml_object.type2
        form.instance.type3 = kycandaml_object.type3
        form.instance.type4 = kycandaml_object.type4
        form.instance.type5 = kycandaml_object.type5
        form_object = form.save()
        form_data = form.cleaned_data
        form_data.update(**kycandaml_object)
        form_data.update(**APIKEY)
        r = requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/updateKycAml',
                          data=form_data)
        json = r.json()
        json_dict = dict(json['Financial Party details'].items())
        del json['Financial Party details']
        json.update(**json_dict)
        serializer = PerformKYCandAMLPartyCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return super().form_valid(form)


class LinkCreateView(CreateView):
    form_class = LinkCreateForm
    template_name = 'transact/link_create.html'
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        account_object = user_object.account.get(user__pk=self.request.user.pk)
        party_object = user_object.party.get(user__pk=self.request.user.pk)
        # form.instance.user = self.request.user
        form.instance.firstEntryType = 'Account'
        form.instance.firstEntry = account_object.accountId
        # if
        form.instance.relatedEntryType = 'IndivACParty'
        form.instance.relatedEntry = party_object.partyId
        form_object = form.save()
        form_data = form.cleaned_data
        form_data.update(**APIKEY)
        form_data.update(**form_object.__dict__)
        r = requests.put('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/createLink',
                         data=form_data)
        json = r.json()
        json_dict = dict(json['linkDetails'][1][0].items())
        del json['linkDetails']
        json_dict['linkId'] = json_dict['id']
        json.update(**json_dict)
        serializer = LinkCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return super().form_valid(form)


class UploadAccountDocumentView(CreateView):
    form_class = UploadAccountDocumentForm
    template_name = 'transact/upload_account_document_create.html'
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        
        form_object = form.save()
        form_data = form.cleaned_data
        
        form_data.update(**APIKEY)
        r = requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/uploadAccountDocument',
                         data=form_data)
      
        return super().form_valid(form)

class TradeCreateView(CreateView):
    form_class = TradeCreateForm
    template_name = "transact/trade_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        
        form.instance.createdIpAddress = get_client_ip(self.request)
        form_object = form.save()
        form_data = form_object.__dict__
        form_data.update(**APIKEY)
        r = requests.post('https://api-sandboxdash.norcapsecurities.com/tapiv3/index.php/v3/createTrade',
                         data=form_data)
        json = r.json()
        json_dict = dict(json['purchaseDetails'][1][0].items())
        del json['purchaseDetails']
        json.update(**json_dict)
        serializer = TradeCreateSerializer(data=json)
        if serializer.is_valid():
            serializer.update(instance=form_object, validated_data=serializer.validated_data)
        return super().form_valid(form)
