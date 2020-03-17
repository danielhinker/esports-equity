from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from accounts.choices import*
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.conf import settings
from teams.models import *
import django.db.models.deletion



class UserManager(BaseUserManager):

    # def get_by_natural_key(self, email):
    #     username = self.get(username__iexact=username)
    #     if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
    #         raise forms.ValidationError(u'Username "%s" is already in use.' % username)
    #     return username.lower()


    # def lowercase_username(self, email):
    #     return email.lower()

    def create_user(self, username, password=None):

        if not username:
            raise ValueError("Users must have an email address")
        # if not display_name:
        #     display_name = username

        user = self.model(
            username=self.normalize_email(username),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(_('email'), unique=True)
    # email = models.EmailField(_('email'), unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # username = models.CharField(max_length=40, unique=True)
    # display_name = models.CharField(max_length=140)
    # is_accredited = models.BooleanField(blank=True, default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(blank=False, default=False)
    email_id = models.CharField(max_length=255, blank=True)
    accepted_tos = models.BooleanField(blank=False, default=False)
    bio = models.TextField(max_length=140, blank=True)
    avatar = models.ImageField(upload_to='media/images/avatars/', blank=True, null=True)
    company_name = models.CharField(blank=True, max_length=150)


    objects = UserManager()

    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ["display_name", "username"]

    def __str__(self):
        return self.username
    #
    def get_full_name(self):
        return self.username
    #
    def get_short_name(self):
        return self.username

class StripeUserID(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='stripe_user_id', blank=True, null=True, on_delete=django.db.models.deletion.CASCADE)
    stripe_user_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.stripe_user_id

class Follow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', blank=True, null=True, on_delete=django.db.models.deletion.CASCADE)
    project = models.ForeignKey(Team, related_name='followed_by', blank=True, null=True, on_delete=django.db.models.deletion.CASCADE)


class Activation(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=django.db.models.deletion.CASCADE) #1 to 1 link with Django User
    activation_key = models.CharField(max_length=255)
    key_expires = models.DateTimeField()