from __future__ import unicode_literals
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.template import Template, Context
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import ProfileUpdateForm

from django.forms import BaseFormSet, formset_factory
from .forms import *
from .serializer import MailChimpSerializer
from .forms import *
from .models import *
import stripe
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from eeweb.settings import *
from eeweb.settings import client_secret
from django.core.mail import send_mail
from django.utils import timezone
import boto3
botoclient = boto3.client('ses', region_name='us-east-1')

import uuid
import hashlib
import random

stripe.api_key = client_secret


class LoginView(generic.FormView):
    form_class = PickyAuthenticationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/login.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy("logout_success")
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class SignUp(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("signup_success")
    template_name = "landing/signup.html"

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            email = self.object.username
            fname = self.object.first_name
            lname = self.object.last_name
          
            data = {}
            data['username'] = email
            salt = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
            usernamesalt = data['username']
            if isinstance(usernamesalt, str):
                usernamesalt = usernamesalt.encode('utf-8')
            data['activation_key'] = hashlib.sha256(salt.encode('utf-8') + usernamesalt).hexdigest()
            data['email_path'] = "/ActivationEmail.txt"
            data['email_subject'] = "Esports Equity Account Activation"
            message = '\n' + 'Thank you for signing up on Esports Equity\n' +\
                      'Activate your account by clicking on this link!\n'
            link = "https://www.esportsequity.com/accounts/activate/" + data['activation_key'] + '\n' + '\n'
            c = Context({'activation_link': link, 'username': data['username']})
            f = open(MEDIA_ROOT + data['email_path'], 'w')
            f.write(message)
            f.write(link)
            f.close()
            f = open(MEDIA_ROOT + data['email_path'], 'r')
            t = Template(f.read())
            f.close()
            message = t.render(c)
            print(str(message).encode('utf8'))
            send_mail(data['email_subject'], message, 'no-reply@esportsequity.com', [data['username']],
                      fail_silently=False)
            
            form.save(data)  # Save the user and his profile
            profile = Activation()
            profile.user = self.object
            profile.activation_key = data['activation_key']
            profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2),
                                                             "%Y-%m-%d %H:%M:%S")
            profile.save()

            success_url = self.get_success_url()

            return HttpResponseRedirect(success_url)
            

def new_activation_link(request):
    data={}
    user = User.objects.get(pk=request.user.pk)
    if user is not None and not user.is_active:
        data['username']=user.username
        data['email_path']="/ResendEmail.txt"
        data['email_subject']="Esports Equity New Activation Link"

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = data['username']
        if isinstance(usernamesalt):
            usernamesalt = usernamesalt.encode('utf8')
        data['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()

        profile = Activation.objects.get(user=user)
        profile.activation_key = data['activation_key']
        profile.key_expires = timezone.now() + timezone.timedelta(days=2)
        profile.save()

        link = "http://www.esportsequity.com/accounts/activate/" + data['activation_key']
        c = Context({'activation_link': link, 'username': data['username']})
        f = open(MEDIA_ROOT + data['email_path'], 'r')
        t = Template(f.read())
        f.close()
        message = t.render(c)
        send_mail(data['email_subject'], message, 'no-reply@esportsequity.com', [data['email']],
                  fail_silently=False)

        request.session['new_link']=True 

    return reverse_lazy("home")


def activation(request, key):
    activation_expired = False
    already_active = False
    profile = get_object_or_404(Activation, activation_key=key)
    if not profile.user.is_active == True:
        if timezone.now() > profile.key_expires:
            activation_expired = True 
            id_user = profile.user.id
        else: #Activation successful
            profile.user.is_active = True
            profile.user.save()

    #If user is already active, simply display error message
    else:
        already_active = True #Display : error message
    return render(request, "registration/email-verified.html")


from django.utils.crypto import get_random_string


def generate_activation_key(username):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(20, chars)
    return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()


def MailchimpSubscribe(request):
    success_url = reverse_lazy("subscribe_success")
    email = str(request.user.email_id)
    fname = request.user.first_name
    lname = request.user.last_name
    User = get_user_model()
    merge_f = {
        'FNAME': fname,
        'LNAME': lname,
    }
    email_hash = request.user.email_id
    status = 'subscribed'

    client.lists.members.update(list_id='8b261363fb', subscriber_hash=email_hash, data={'email_address':request.user.email,'status': 'subscribed'})
    request.user.is_subscribed = True
    request.user.save()
    return HttpResponseRedirect(success_url)


def MailchimpUnsubscribe(request):
    success_url = reverse_lazy("unsubscribe_success")
    email = str(request.user.email_id)
    fname = request.user.first_name
    lname = request.user.last_name
    User = get_user_model()
    merge_f = {
        'FNAME': fname,
        'LNAME': lname,
    }
    email_hash = request.user.email_id
    status = 'subscribed'

    client.lists.members.update(list_id='8b261363fb', subscriber_hash=email_hash, data={'email_address':request.user.email,'status': 'unsubscribed'})
    request.user.is_subscribed = False
    request.user.save()
    return HttpResponseRedirect(success_url)


def change_password(request):
    object = request.user.get_username()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/setting/account-dashboard.html', {
        'object': object,
        'form': form
    })


class AccountDelete(generic.DeleteView):
    model = User
    template_name = "accounts/delete_account.html"
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        object = get_object_or_404(User, pk=self.request.user.pk)
        return object


@login_required(login_url='/accounts/login/')
def ProfilePage(request, profile_pk):
    user_object = get_object_or_404(User, pk=profile_pk)
    user_teams = user_object.team.all()
    user_backings = user_object.backings.all()
    backed_projects = []
    for backing in user_backings:
        backed_projects.append(backing.project)

    return render(request, 'accounts/profile.html', {'user_teams': user_teams,
                                                     'backed_projects': backed_projects, 'profile_pk': profile_pk,
                                                     'user_object': user_object})

class ProfileSettings(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    form_class = ProfileUpdateForm
    template_name = "accounts/setting/profile_settings.html"
    success_url = reverse_lazy('accounts:profile_settings')
    
    def get_object(self, queryset=None):
        return self.request.user


class NameChangeSettings(generic.UpdateView):
    model = User
    template_name = 'accounts/change_name.html'
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('accounts:profile_settings')


    def get_object(self, queryset=None):
        return self.request.user


class DescriptionChangeSettings(generic.UpdateView):
    model = User
    template_name = 'accounts/change_name.html'
    fields = ['bio']
    success_url = reverse_lazy('accounts:profile_settings')

    def get_object(self, queryset=None):
        return self.request.user


class ProjectCreateView2(UpdateView):
    form_class = ProjectCreateForm2
    template_name = 'accounts/project_update/second_step.html'

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))
        return project_object

    def get_success_url(self):
        return reverse("accounts:create_project_3", args=(self.object.pk,))


class ProjectCreateView3(UpdateView):
    form_class = ProjectCreateForm3
    template_name = 'accounts//project_update/third_step.html'

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))
        return project_object

    def get_success_url(self):
        return reverse("accounts:create_project_4", args=(self.object.pk,))


class ProjectCreateView4(CreateView):
    form_class = ProjectCreateForm4
    template_name = 'accounts/project_update/fourth_step.html'

    def form_valid(self, form):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('pk'))
        form.instance.project = project_object
        form_object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("accounts:create_project_5", args=(self.kwargs.get('project_pk'),))


class ProjectCreateView5(UpdateView):
    form_class = ProjectCreateForm5
    template_name = 'accounts/project_update/fifth_step.html'

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))

        return project_object

    def get_success_url(self):
        return reverse("accounts:create_project_6", args=(self.object.pk,))


class ProjectCreateView6(UpdateView):
    form_class = ProjectCreateForm6
    template_name = 'accounts/project_update/sixth_step.html'
    # success_url = reverse_lazy("teams:create_party_3")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))
        return project_object

    def get_success_url(self):
        return reverse("home")

def RewardsCreate(request, project_pk):
    user_object = get_object_or_404(User, pk=request.user.pk)
    project_object = user_object.team.get(pk=project_pk)
    reward_object = project_object.reward.all()

    RewardFormSet = modelformset_factory(Reward, fields=('reward_title', 'reward_amount', 'reward_description',
                                                         'estimated_delivery', 'shipping_details',))

    if request.method == 'POST':
        formset = RewardFormSet(request.POST)
        if formset.is_valid():
            # formset.project = project_object
            # formset.save()
            instances = formset.save(commit=False)
            for form in instances:
                form.project = project_object
                form.save()

            return HttpResponseRedirect(reverse("teams:create_project_5", args=(project_pk,)))

    else:
        formset = RewardFormSet(queryset=Reward.objects.filter(project__pk=project_pk))

    return render(request, 'accounts/project_update/fourth_step.html', {
        'reward_object': reward_object,
        'project_object': project_object,
        'team': project_object,
        'project_pk': project_pk,
        'formset': formset,
    })



class ProjectDeleteView(DeleteView):
    model = Team

    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))
        return project_object

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("home")
