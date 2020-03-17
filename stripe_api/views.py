from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)

from django.urls import reverse_lazy

from django.views.generic import TemplateView

from django.http import HttpResponseRedirect
from django.contrib import messages
from eeweb.settings import client_secret

from .forms import *
from .serializer import *
from .models import *
from accounts.models import User
from django.shortcuts import redirect
from django.db.models import F
from teams.models import *
from teams.forms import *

import stripe

stripe.api_key = client_secret

def stripe_customer(request):
    pass

def stripe_page(request, project_pk):
    form = ChargeCreateForm2()
    if request.method == 'POST':
        form = ChargeCreateForm2(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            project_pk = project_pk
            return render(request, 'stripe_api/invest_in_team_2.html', context={'amount': amount, 'project_pk': project_pk})
    return render(request, 'stripe_api/invest_in_team.html', context={'form': form})

def stripe_charge_2(request):
   
    if request.method == 'POST':
   
        amount = request.POST['amount']
        project_pk = request.POST['project_pk']


    return HttpResponseRedirect(reverse_lazy('stripe_api:back_team_3'))


def stripe_charge_3(request):
  
    print(request.POST)
    token = request.POST['stripeToken']
    amount = request.POST['amount']
    project_pk = request.POST.get("project_pk", "")
    user_object = get_object_or_404(User, pk=request.user.pk)
    project_object = Team.objects.get(pk=request.POST.get("project_pk", ""))
    stripe.api_key = client_secret
    charge = stripe.Charge.create(
        amount=(int(amount) * 100),
        currency='usd',
        source=token,
        description=project_object.title,
    )

    if request.POST.get("reward_pk", ""):
        reward_object = Reward.objects.get(pk=request.POST.get("reward_pk", ""))

    
    form_data = {'amount': (int(amount) / 100)}

    form = BackProjectForm1(form_data)
    if form.is_valid():
        form_instance = form.save(commit=False)
        form_instance.project = project_object
        if request.POST.get("reward_pk", ""):
            form_instance.reward = reward_object
        form_instance.user = user_object
        form_saved = form_instance.save()

        project_object.current_raise = F('current_raise') + (int(amount)/100)
    
        project_object.save()

    return HttpResponseRedirect(reverse_lazy('stripe_api:back_success'))
    

class BackSuccess(TemplateView):
    template_name = "stripe_api/thank-you.html"


def BackPage(request, project_pk):
    team = get_object_or_404(Team, pk=project_pk)
    days_left = (team.duration - datetime.datetime.now().date()).days

    return render(request, 'stripe_api/back-page.html',
                  {'team': team, 'days_left': days_left,})


def BackPage2(request, project_pk):
    team = get_object_or_404(Team, pk=project_pk)
    days_left = (team.duration - datetime.datetime.now().date()).days
    amount = request.POST['amount']
    project_pk = request.POST['project_pk']
   
    return render(request, 'stripe_api/back-page-2.html',
                  {'team': team, 'days_left': days_left, 'amount': amount, 'message': message})

