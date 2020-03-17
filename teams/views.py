from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView, RedirectView
)
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _

from eeweb.settings import client_secret
from django.forms import BaseFormSet, formset_factory, modelformset_factory
from django.db.models import F
from stripe_api.serializer import *

import requests
from accounts.models import User


class AllTeams(ListView):
    model = Team
    context_object_name = 'team_list'
    paginate_by = 9
    queryset = Team.objects.all()


class ExploreView(generic.ListView):
    model = Team
    template_name = 'teams/explore.html'
    context_object_name = 'team_list'
    paginate_by = 8


    def get_queryset(self):
        team_objects = Team.objects.all()
        verified_team_list = []
        for team in team_objects:
            if team.is_verified and team.duration >= datetime.datetime.now().date():
                verified_team_list.append(team)
     

        return verified_team_list



def DetailTeam(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    days_left = (team.duration - datetime.datetime.now().date()).days
    try:
        reward_objects = team.reward.all().order_by('reward_amount')[::0]
    except:
        backing_objects = team.backed_by.all().order_by('-created_at')

        return render(request, 'teams/project.html',
                      {'team': team, 'backing_objects': backing_objects})
    else:
        backing_objects = team.backed_by.all().order_by('-created_at')

        return render(request, 'teams/project.html',
                      {'team': team, 'reward_objects': reward_objects,
                       'backing_objects': backing_objects, 'project_pk': team_id,
                       'days_left': days_left})


@login_required(login_url='/accounts/login/')
def follow_team(request, team_id):
    user_object = get_object_or_404(User, pk=request.user.pk)
    team = get_object_or_404(Team, pk=team_id)
   
    form = BackProjectForm1()
    if form.is_valid():
        form_instance = form.save(commit=False)
        form_instance.project = team
        form_instance.user = user_object
    
        form_saved = form_instance.save()

   
    return HttpResponseRedirect(reverse_lazy('teams:detail', args=team_id))

@login_required(login_url='/accounts/login/')
def all_follow(request):
    following = request.user.followers.all()
    return render(request, 'accounts/profile/account-profile.html', {'follow': following})


@login_required(login_url='/accounts/login/')
def unfollow_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.following.remove(request.user)
    team.save()
    return render(request, 'teams/detail.html', {'team':team})


class ProjectCreateView(CreateView):
    form_class = ProjectCreateForm1
    template_name = 'teams/project_creation/first_step.html'

    def form_valid(self, form):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        form.instance.user = user_object
        form_object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("teams:create_project_2", args=(self.object.pk,))


class ProjectCreateView2(UpdateView):
    form_class = ProjectCreateForm2
    template_name = 'teams/project_creation/second_step.html'
    
    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))
        return project_object

    def get_success_url(self):
        return reverse("teams:create_project_3", args=(self.object.pk,))


class ProjectCreateView3(UpdateView):
    form_class = ProjectCreateForm3
    template_name = 'teams/project_creation/third_step.html'


    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))
        return project_object

    def get_success_url(self):
        return reverse("teams:create_project_4", args=(self.object.pk,))


class ProjectCreateView5(UpdateView):
    form_class = ProjectCreateForm5
    template_name = 'teams/project_creation/fifth_step.html'

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))

        return project_object

    def form_valid(self, form):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))
        if not user_object.bio:
            user_object.bio = form.instance.profile_biography
        if not user_object.avatar:
            user_object.avatar = form.instance.profile_image

        form_object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("teams:create_project_6", args=(self.object.pk,))


class ProjectCreateView6(UpdateView):
    form_class = ProjectCreateForm6
    template_name = 'teams/project_creation/sixth_step.html'
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))
        return project_object


class ProjectDeleteView(DeleteView):

    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))
        return project_object

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("teams:create_project")

def BackView(request, project_pk):
    team = get_object_or_404(Team, pk=project_pk)
    try:
        reward_objects = team.reward.all().order_by('reward_amount')[::0]
    except:
        backing_objects = team.backed_by.all().order_by('created_at')
   
        return render(request, 'teams/project.html',
                      {'team': team, 'backing_objects': backing_objects})
    else:
        backing_objects = team.backed_by.all().order_by('created_at')

    return render(request, 'teams/back-page.html',
                  {'team': team, 'reward_objects': reward_objects,  'backing_objects': backing_objects})


def RewardsCreate(request, project_pk):
    user_object = get_object_or_404(User, pk=request.user.pk)
    project_object = user_object.team.get(pk=project_pk)
    reward_object = project_object.reward.all()

    RewardFormSet = modelformset_factory(Reward, form=ProjectCreateForm4)


    if request.method == 'POST':
        formset = RewardFormSet(request.POST)
        if formset.is_valid():
            
            instances = formset.save(commit=False)
            for form in instances:
                form.project = project_object
                form.save()

            return HttpResponseRedirect(reverse("teams:create_project_5", args=(project_pk,)))

    else:
        formset = RewardFormSet(queryset=Reward.objects.filter(project__pk=project_pk))

    return render(request, 'teams/project_creation/fourth_step.html', {
        'reward_object': reward_object,
        'project_object': project_object,
        'team': project_object,
        'project_pk': project_pk,
        'formset': formset,
    })


class RewardsDeleteAllView4(DeleteView):
   
    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))
        reward_object = project_object.reward.all()
        return reward_object

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse("teams:create_project_4", args=(self.kwargs.get('project_pk'),))


class RewardsDeleteView4(DeleteView):
  
    def get_object(self, queryset=None):
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        project_object = user_object.team.get(pk=self.kwargs.get('project_pk'))
        reward_object = project_object.reward.get(pk=self.kwargs.get('reward_pk'))
        return reward_object

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse("teams:create_project_4", args=(self.kwargs.get('project_pk'),))


def RewardsList(request, project_pk):
    team = get_object_or_404(Team, pk=project_pk)
    try:
        reward_objects = team.reward.all().order_by('reward_amount')[::0]
    except:
        return render(request, 'teams/project_creation/fourth_step_update.html',
                      {'team': team, })
    else:

        return render(request, 'teams/project_creation/fourth_step_update.html',
                      {'team': team, 'reward_objects': reward_objects, })


class ProjectSuccessView7(generic.ListView):
    model = Team
    template_name = "teams/project_creation/project-inspect.html"
    context_object_name = 'team_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        user_object = get_object_or_404(User, pk=self.request.user.pk)
        context = super().get_context_data(**kwargs)
        context['code'] = self.request.GET.get('code', '')
        form_data = {'client_secret': client_secret, 'code': context['code'], 'grant_type': 'authorization_code'}
        r = requests.post('https://connect.stripe.com/oauth/token',
                          data=form_data)
        json = r.json()
        serializer = StripeSerializer(data=json)
        if serializer.is_valid():
            saved_serializer = serializer.save()
            saved_serializer.user = user_object
            saved_serializer = serializer.save()

        print(context['code'])

        return context
