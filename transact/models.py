from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
from accounts.models import User
import django.db.models.deletion
from .choices import *


class MyClass(models.Model):
    accountRegistration = models.CharField(max_length=255)
    createdIpAddress = models.CharField(max_length=255)


class Party(models.Model):
    user = models.ForeignKey(User, related_name='party', on_delete=django.db.models.deletion.CASCADE)
    domicile = models.CharField(choices=Domicile, max_length=255)
    firstName = models.CharField(max_length=255)
    middleInitial = models.CharField(max_length=1, blank=True)
    lastName = models.CharField(max_length=255)
    socialSecurityNumber = models.CharField(max_length=255, blank=True)
    dob = models.CharField(max_length=255, blank=True)
    primCountry = models.CharField(max_length=255)
    primAddress1 = models.CharField(_('address'), max_length=255)
    primAddress2 = models.CharField(_('address 2'), max_length=255, blank=True)
    primCity = models.CharField(max_length=255)
    primState = models.CharField(max_length=2)
    primZip = models.CharField(max_length=5)
    emailAddress = models.CharField(max_length=255)
    emailAddress2 = models.CharField(max_length=255, blank=True)
    phone = models.IntegerField(blank=True, null=True)
    phone2 = models.IntegerField(blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    associatedPerson = models.NullBooleanField(blank=True)
    empCountry = models.CharField(max_length=255, blank=True, null=True)
    empAddress1 = models.CharField(max_length=255, blank=True, null=True)
    empAddress2 = models.CharField(max_length=255, blank=True, null=True)
    empCity = models.CharField(max_length=255, blank=True, null=True)
    empState = models.CharField(max_length=2, blank=True, null=True)
    empZip = models.CharField(max_length=5, blank=True, null=True)
    empName = models.CharField(max_length=255, blank=True, null=True)
    invest_to = models.NullBooleanField(blank=True)
    currentAnnIncome = models.IntegerField(blank=True, null=True)
    avgAnnIncome = models.IntegerField(blank=True, null=True)
    currentHouseholdIncome = models.IntegerField(blank=True, null=True)
    householdNetworth = models.IntegerField(blank=True, null=True)

    createdIpAddress = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(max_length=255, blank=True)

    partyId = models.CharField(max_length=255, null=True, blank=True)
    # phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
    # error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))

    class Meta:
        verbose_name = 'Party'
        verbose_name_plural = 'Parties'

    def __str__(self):
        return self.user.username


class Entity(models.Model):
    user = models.ForeignKey(User, related_name='entity', on_delete=django.db.models.deletion.CASCADE)
    domicile = models.CharField(choices=Entity_Domicile, max_length=255)
    entityName = models.CharField(max_length=255)
    entityType = models.CharField(choices=Entity_Type, max_length=255)
    entityDesc = models.CharField(max_length=255)
    ein = models.IntegerField(blank=True, null=True)
    primCountry = models.CharField(max_length=255)
    primAddress1 = models.CharField(_('address'), max_length=255)
    primAddress2 = models.CharField(_('address 2'), max_length=255, blank=True)
    primCity = models.CharField(max_length=255)
    primState = models.CharField(max_length=2)
    primZip = models.CharField(max_length=5)
    emailAddress = models.CharField(max_length=255)
    emailAddress2 = models.CharField(max_length=255, blank=True)
    phone = models.IntegerField(blank=True, null=True, validators=[
        RegexValidator(
            regex='^\d{10}$',
            message='Phone number must be 10 digits',
            code='invalid_phonenumber'
            ),
        ]
    )
    phone2 = models.IntegerField(blank=True, null=True, validators=[
        RegexValidator(
            regex='^\d{10}$',
            message='Phone number must be 10 digits',
            code='invalid_phonenumber'
            ),
        ]
    )
    totalAssets = models.IntegerField(blank=True, null=True)
    ownersAI = models.CharField(choices=Owners_AI, max_length=255)
    KYCstatus = models.CharField(choices=KYCstatus, max_length=255, default='Pending', null=True, blank=True)
    AMLstatus = models.CharField(choices=AMLstatus, max_length=255, default='Pending', null=True, blank=True)
    AMLdate = models.TimeField(blank=True, null=True)
    createdIpAddress = models.CharField(max_length=255)
    partyId = models.CharField(max_length=255, blank=True)


    class Meta:
        verbose_name = 'Entity'
        verbose_name_plural = 'Entities'

    def __str__(self):
        return self.user.username


class Account(models.Model):
    user = models.ForeignKey(User, related_name='account', on_delete=django.db.models.deletion.CASCADE)
    # party = models.ForeignKey(Party, related_name='account', null=True, blank=True)
    # entity = models.ForeignKey(Entity, related_name='account', null=True, blank=True)
    accountRegistration = models.CharField(max_length=255, blank=True)
    type = models.CharField(choices=Account_Type, max_length=255, blank=True)
    entityType = models.CharField(choices=Entity_Type, max_length=255, blank=True)
    domesticYN = models.CharField(choices=Domestic, max_length=255, blank=True)
    streetAddress1 = models.CharField(max_length=255, blank=True)
    streetAddress2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    phone = models.IntegerField(blank=True, null=True, validators=[
        RegexValidator(
            regex='^\d{10}$',
            message='Phone number must be 10 digits',
            code='invalid_phonenumber'
            ),
        ]
    )
    taxID = models.IntegerField(blank=True, null=True)
    KYCstatus = models.CharField(choices=KYCstatus, max_length=255, default='Pending')
    AMLstatus = models.CharField(choices=AMLstatus, max_length=255, default='Pending')
    AMLdate = models.TimeField(null=True, blank=True)
    suitabilityScore = models.IntegerField(blank=True, null=True)
    suitabilityDate = models.TimeField(null=True, blank=True)
    suitabilityApprover = models.CharField(max_length=255, blank=True)
    AccreditedStatus = models.CharField(choices=Accredited_Status, max_length=255, blank=True, default='Pending')
    Allow = models.CharField(choices=Allow_Status, max_length=255, blank=True)
    Aldate = models.TimeField(null=True, blank=True)
    c506Limit = models.IntegerField(null=True, blank=True)
    accountTotalLimit = models.IntegerField(blank=True, null=True)
    singleInvestmentLimit = models.IntegerField(blank=True, null=True)
    associatedAC = models.CharField(choices=Associated_AC, max_length=255, blank=True)
    syndicate = models.CharField(choices=Syndicate, max_length=255, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    # notes = models.CharField(max_length=255)
    approvalStatus = models.CharField(choices=Approval_Status, max_length=255, default='Pending')
    approvalLastReview = models.TimeField(null=True, blank=True)

    accountId = models.CharField(max_length=255, blank=True)
    updatedIpAddress = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.user.username


class Issuer(models.Model):
    user = models.ForeignKey(User, related_name='issuer', on_delete=django.db.models.deletion.CASCADE)
    issuerName = models.CharField(max_length=30, blank=False)
    firstName = models.CharField(max_length=30, blank=False)
    lastName = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=False, blank=False)
    issuerId = models.IntegerField(blank=False, null=True)
    issuerStatus = models.CharField(max_length=30, blank=True, null=False)
    # phoneNumber = models.IntegerField(blank=True, null=True)
    createdIpAddress = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.issuerName


class IssuerAccount(models.Model):
    issuer = models.ForeignKey(Issuer, related_name='issuer_account', on_delete=django.db.models.deletion.CASCADE)
    accountType = models.CharField(max_length=255)
    companyName = models.CharField(max_length=255)
    companyState = models.CharField(max_length=255)
    # entityType =
    companyTaxID = models.IntegerField(blank=False, null=True)
    accountMiddleInitial = models.CharField(max_length=1)
    # socialSecurityNumber
    # dob
    residentUS = models.CharField(choices=Resident_US, max_length=255)
    citizenUS = models.CharField(choices=Citizen_US, max_length=255)
    addressline1 = models.CharField(_('address'), max_length=255)
    addressline2 = models.CharField(_('address 2'), max_length=255, blank=True)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    country = models.CharField(max_length=255)
    issuingCountry = models.CharField(max_length=255)
    issuerId = models.IntegerField(blank=True, null=True)
    issuerStatus = models.CharField(max_length=30, blank=True, null=False)

    def __str__(self):
        return self.issuer.email


class Offering(models.Model):
    issuer = models.ForeignKey(Issuer, related_name='offering', on_delete=django.db.models.deletion.CASCADE)
    issuerId = models.IntegerField(blank=True, null=True)
    issueName = models.CharField(max_length=255, blank=False)
    issueType = models.CharField(choices=Issue_Type, max_length=255, blank=False)
    targetAmount = models.DecimalField(decimal_places=2, max_digits=255, validators=[MinValueValidator(Decimal('0.01'))])
    minAmount = models.DecimalField(decimal_places=2, max_digits=255, validators=[MinValueValidator(Decimal('0.01'))])
    maxAmount = models.DecimalField(decimal_places=2, max_digits=255, validators=[MinValueValidator(Decimal('0.01'))])
    unitPrice = models.DecimalField(decimal_places=2, max_digits=255, validators=[MinValueValidator(Decimal('0.01'))])
    startDate = models.CharField(max_length=255, blank=True)
    endDate = models.CharField(max_length=255, blank=True)
    offeringText = models.CharField(max_length=255, blank=True)
    stampingText = models.CharField(max_length=255, blank=True)
    createdIPAddress = models.CharField(max_length=255, blank=True, null=True)

    offeringId = models.CharField(max_length=255, blank=True)
    offeringStatus = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.issueName


class EscrowAccount(models.Model):
    offering = models.ForeignKey(Offering, related_name='escrow_account', on_delete=django.db.models.deletion.CASCADE)
    offeringId = models.IntegerField()
    overFundingAmount = models.DecimalField(decimal_places=2, max_digits=255)
    bankName = models.CharField(max_length=255, blank=True)
    offeringAccountNumber = models.CharField(max_length=255, blank=True)
    accountFullName = models.CharField(max_length=255, blank=True)

    issuerId = models.IntegerField(blank=True, null=True)
    escrowAccountStatus = models.CharField(max_length=255, blank=True)


class ExternalAccount(models.Model):
    account = models.ForeignKey(Account, related_name='external_account', on_delete=django.db.models.deletion.CASCADE)
    issuer = models.ForeignKey(Issuer, related_name='external_account', on_delete=django.db.models.deletion.CASCADE)
    types = models.CharField(choices=External_Account_Type, max_length=255, blank=True)
    accountId = models.CharField(max_length=255, blank=True)
    ExtAccountfullname = models.CharField(max_length=255, blank=True)
    Extnickname = models.CharField(max_length=255, blank=True)
    ExtRoutingnumber = models.CharField(max_length=255, blank=True)
    ExtAccountnumber = models.CharField(max_length=255, blank=True)
    updatedIpAddress = models.CharField(max_length=255, blank=True, null=True)

    statusCode = models.CharField(max_length=255, blank=True)
    statusDesc = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.ExtAccountfullname


class UploadAccountDocument(models.Model):
    account = models.ForeignKey(Account, related_name='upload_account_document', on_delete=django.db.models.deletion.CASCADE)
    accountId = models.CharField(max_length=255, blank=True)
    documentTitle = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    userfile0 = models.FileField(null=True, blank=True)

    document_details = models.CharField(max_length=255, blank=True)


class UploadEntityDocument(models.Model):
    entity = models.ForeignKey(Entity, related_name='upload_entity_document', on_delete=django.db.models.deletion.CASCADE)
    partyId = models.CharField(max_length=255)
    documentTitle = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    userfile0 = models.CharField(max_length=255)
    createdIpAddress = models.CharField(max_length=255)

    document_details = models.CharField(max_length=255)


class UploadPartyDocument(models.Model):
    party = models.ForeignKey(Party, related_name='upload_party_document', on_delete=django.db.models.deletion.CASCADE)
    partyId = models.CharField(max_length=255)
    documentTitle = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    userfile0 = models.CharField(max_length=255)
    createdIpAddress = models.CharField(max_length=255)
    document_details = models.CharField(max_length=255)


class DocumentsOffering(models.Model):
    offeringId = models.CharField(max_length=255)
    documentTitle = models.CharField(max_length=255)
    documentFileReferenceCode = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    userfile0 = models.CharField(max_length=255)
    createdIpAddress = models.CharField(max_length=255)

    documentURL = models.CharField(max_length=255)
    documentId = models.CharField(max_length=255)


class KYCandAML(models.Model):
    party = models.ForeignKey(Party, related_name='KYCandAML', blank=True, null=True, on_delete=django.db.models.deletion.CASCADE)
    statusCode = models.CharField(max_length=255)
    statusDesc = models.CharField(max_length=255)
    partyId = models.CharField(max_length=255)

    kycStatus = models.CharField(max_length=255, default='Pending')
    AML = models.CharField(max_length=255)
    noOfqns = models.IntegerField(blank=True, null=True)
    idNumber = models.IntegerField(blank=True, null=True) # KYC Generated ID number

    prompt1 = models.CharField(max_length=255, blank=True)
    type1 = models.CharField(max_length=255, blank=True)
    answer1 = models.CharField(max_length=255, blank=True)
    qns1 = models.CharField(max_length=255, blank=True)

    prompt2 = models.CharField(max_length=255, blank=True)
    type2 = models.CharField(max_length=255, blank=True)
    answer2 = models.CharField(max_length=255, blank=True)
    qns2 = models.CharField(max_length=255, blank=True)

    prompt3 = models.CharField(max_length=255, blank=True)
    type3 = models.CharField(max_length=255, blank=True)
    answer3 = models.CharField(max_length=255, blank=True)
    qns3 = models.CharField(max_length=255, blank=True)

    prompt4 = models.CharField(max_length=255, blank=True)
    type4 = models.CharField(max_length=255, blank=True)
    answer4 = models.CharField(max_length=255, blank=True)
    qns4 = models.CharField(max_length=255, blank=True)

    prompt5 = models.CharField(max_length=255, blank=True)
    type5 = models.CharField(max_length=255, blank=True)
    answer5 = models.CharField(max_length=255, blank=True)
    qns5 = models.CharField(max_length=255, blank=True)


class Suitability(models.Model):
    account = models.ForeignKey(Account, related_name='suitability', on_delete=django.db.models.deletion.CASCADE)
    accountId = models.CharField(max_length=255, blank=True)
    riskProfile = models.CharField(choices=Risk_Profile, max_length=255)
    investmentExperience = models.CharField(choices=Investment_Experience, max_length=255)
    privOffExperience = models.CharField(choices=Priv_Off_Experience, max_length=255)
    pctPrivSecurities = models.IntegerField(blank=True)
    pctIlliquidSecurities = models.IntegerField(blank=True)
    pctRealEstate = models.IntegerField(blank=True)
    timeHorizon = models.IntegerField(blank=True)
    education = models.CharField(choices=Education, max_length=255)
    financialAdvisor = models.CharField(choices=Financial_Advisor, max_length=255)


class Trade(models.Model):
    offeringId = models.CharField(max_length=255, blank=True)
    accountId = models.CharField(max_length=255, blank=True)
    transactionType = models.CharField(choices=Trade_Type, max_length=255, blank=True)
    transactionUnits = models.CharField(max_length=255, blank=True)
    createdIpAddress = models.CharField(max_length=255, blank=True, null=True)
    funds = models.CharField(max_length=255, blank=True)
    tradeId = models.CharField(max_length=255, blank=True)
    partyId = models.CharField(max_length=255, blank=True)
    transactionId = models.CharField(max_length=255, blank=True)
    transactionAmount = models.CharField(max_length=255, blank=True)
    transactionDate = models.DateTimeField(max_length=255, blank=True, null=True, default=timezone.now)
    transactionStatus = models.CharField(max_length=255, blank=True)
    TradeFinancialDetails = models.CharField(max_length=255, blank=True)
    orderStatus = models.CharField(max_length=255, blank=True)


class Link(models.Model):
    firstEntryType = models.CharField(max_length=255, blank=True)
    firstEntry = models.CharField(max_length=255, blank=True)
    relatedEntryType = models.CharField(max_length=255, blank=True)
    relatedEntry = models.CharField(max_length=255, blank=True)
    linkType = models.CharField(choices=Link_Type, max_length=255, blank=True, default='owner')
    linkId = models.CharField(max_length=255, blank=True)


# class Abstract(models.Model):
#     created_at
#     modified_at
#     statusCode
#     statusDesc
#
#     class Meta:
#         abstract = True
