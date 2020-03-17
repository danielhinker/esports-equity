from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.utils import timezone
from teams.choices import *
from datetime import timedelta
import datetime
from django.utils import timezone
import django.db.models.deletion
import re
from django.core.validators import RegexValidator



year_dropdown = []
for y in range(1900, datetime.datetime.now().year):
    year_dropdown.append((y, y))

month_dropdown = []
for y in range(1, 13):
    month_dropdown.append((y, y))

day_dropdown = []
for y in range(1, 32):
    day_dropdown.append((y, y))



alphanumeric = RegexValidator(regex='^[a-zA-Z0-9]*$', message='Only alphanumeric characters are allowed for title')

class Team(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='team', blank=True, null=True, on_delete=django.db.models.deletion.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    title = models.CharField(max_length=255, unique=True, blank=True, null=True)

    short_description = models.CharField(blank=True, null=True, max_length=500)
    project_image = models.ImageField(upload_to='media/images/teams/project/image', blank=True, null=True)
    duration = models.DateField(blank=True, null=True)
    project_category = models.CharField(choices=Project_Category, max_length=255, blank=True, null=True)
    project_location = models.CharField(choices=STATES, max_length=2, default='US', blank=True, null=True)
    # roster = models.TextField(blank=True, null=True)
    current_raise = models.IntegerField(blank=True, default=0, null=True)
    category = models.CharField(choices=CATEGORY, max_length=32, null=True, blank=True)
    project_type = models.CharField(choices=Project_Type, max_length=32, null=True, blank=True)
    is_verified = models.BooleanField(default=False, blank=True)
    # state = models.CharField(choices=STATES, null=True, default=None, max_length=2, blank=True)
    # following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True, null=True)
    # gaming_category = models.CharField(choices=Games, max_length=255, blank=True, null=True)
    funding_goal = models.IntegerField(blank=True, default=0, null=True)
    profile_image = models.ImageField(upload_to='media/images/teams/profile/image', blank=True, null=True)
    project_video = models.FileField(upload_to='media/images/project/video', blank=True, null=True)
    project_image_2 = models.ImageField(upload_to='media/images/teams/project/image/secondary', blank=True, null=True)

    profile_biography = models.CharField(max_length=255, blank=True, null=True)
    project_description = models.TextField(max_length=255, blank=True, null=True)
    project_story_background = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class Reward(models.Model):
    project = models.ForeignKey(Team, related_name='reward', blank=True, null=True, on_delete=django.db.models.deletion.CASCADE)
    # list = models.ForeignKey(Reward_list, related_name='reward_item')
    # limit_availability = models.CharField(max_length=255, blank=True, null=True)
    reward_title = models.CharField(max_length=255, blank=True, null=True)
    reward_amount = models.IntegerField(blank=True, null=True)
    reward_description = models.CharField(max_length=255, blank=True, null=True)
    estimated_delivery = models.CharField(max_length=255, blank=True, null=True)
    shipping_details = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.project.title


class BankAccount(models.Model):
    project = models.ForeignKey(Team, related_name='bank_account', on_delete=django.db.models.deletion.CASCADE)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    routing_number = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    account_holder_name = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)
    fund_recipient = models.CharField(choices=Recipient_Type, max_length=255, blank=True, null=True)

    firstName = models.CharField(max_length=255, blank=True, null=True)
    lastName = models.CharField(max_length=255, blank=True, null=True)
    dob = models.CharField(max_length=255, blank=True, null=True)
    dob_day = models.CharField(choices=day_dropdown, max_length=255, blank=True, null=True)
    dob_month = models.CharField(choices=MONTHS, max_length=255, blank=True, null=True)
    dob_year = models.CharField(choices=year_dropdown, max_length=255, blank=True, null=True)
    country = models.CharField(choices=COUNTRIES, max_length=2, default='US', blank=True, null=True)
    address1 = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(choices=STATES, max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)


class Backing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='backings', blank=True, null=True, on_delete=django.db.models.deletion.CASCADE)
    project = models.ForeignKey(Team, related_name='backed_by', blank=True, null=True, on_delete=django.db.models.deletion.CASCADE)
    reward = models.ForeignKey(Reward, related_name='backed_with', blank=True, null=True, on_delete=django.db.models.deletion.CASCADE)
    created_at = models.DateField(default=timezone.now, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    # message = models.CharField(max_length=255, blank=True, null=True)
    # message_is_verified = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.project.title









