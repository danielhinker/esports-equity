from django.urls import include, path, re_path
from django.contrib import admin

from .views import *

app_name = 'transact'
urlpatterns = [
    re_path(r'^account/create/$', AccountCreateView.as_view(), name='account_create'),
    re_path(r'^account/update/$', AccountUpdateView.as_view(), name='account_update'),
    re_path(r'^account/delete/$', AccountDeleteView.as_view(), name='account_delete'),
    re_path(r'^party/create/$', PartyCreateView.as_view(), name='party_create'),
    re_path(r'^party/update/$', PartyUpdateView.as_view(), name='party_update'),
    re_path(r'^party/delete/$', PartyDeleteView.as_view(), name='party_delete'),
    re_path(r'^entity/create/$', EntityCreateView.as_view(), name='entity_create'),
    re_path(r'^entity/update/$', EntityUpdateView.as_view(), name='entity_update'),
    re_path(r'^entity/delete/$', EntityDeleteView.as_view(), name='entity_delete'),
    re_path(r'^issuer/create/$', IssuerCreateView.as_view(), name='issuer_create'),
    re_path(r'^issuer/update/$', IssuerUpdateView.as_view(), name='issuer_update'),
    re_path(r'^issuer/delete/$', IssuerDeleteView.as_view(), name='issuer_delete'),
    re_path(r'^issueraccount/create$', IssuerAccountCreateView.as_view(), name='issuer_account_create'),
    re_path(r'^issueraccount/delete$', IssuerAccountDeleteView.as_view(), name='issuer_account_delete'),
    re_path(r'^offering/create$', OfferingCreateView.as_view(), name='offering_create'),
    re_path(r'^offering/update$', OfferingUpdateView.as_view(), name='offering_update'),
    re_path(r'^offering/delete$', OfferingDeleteView.as_view(), name='offering_delete'),
    re_path(r'^externalaccount/create$', ExternalAccountCreateView.as_view(), name='external_account_create'),
    re_path(r'^externalaccount/update$', ExternalAccountUpdateView.as_view(), name='external_account_update'),
    re_path(r'^externalaccount/delete$', ExternalAccountDeleteView.as_view(), name='external_account_delete'),
    re_path(r'^calculate/suitability$', SuitabilityCalculate.as_view(), name='calculate_suitability'),
    re_path(r'^perform/kycaml/party$', PerformKYCandAMLParty.as_view(), name='perform_kyc_aml_party'),
    re_path(r'^update/kycaml/party$', UpdateKYCandAMLParty.as_view(), name='update_kyc_aml_party'),
    re_path(r'^link/create', LinkCreateView.as_view(), name='link_create'),
    re_path(r'^trade/create', TradeCreateView.as_view(), name='trade_create'),
    re_path(r'^upload/account/document', UploadAccountDocumentView.as_view(), name='upload_account_document'),
    re_path(r'^escrowaccount$', EscrowAccountCreateView.as_view(), name='escrow_account_create'),
    re_path(r'^myform/?$', MyView.as_view(), name='my-form'),
    re_path(r'^issuer/(?P<pk>\d+)/$', IssuerDeleteView.as_view(), name='issuer_delete'),
]