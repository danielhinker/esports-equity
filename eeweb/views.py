from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.db.models import F, FloatField, Sum
import operator


from teams.models import *
from django.views import generic
from accounts.models import *
from teams.models import *


class IndexView(generic.ListView):
    model = Team
    template_name = "teams/indexfund.html"
    context_object_name = 'team_list'



    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        team_objects = Team.objects.all()
        verified_team_list = []
        if team_objects:
            for team in team_objects:
                if team.is_verified and team.duration >= datetime.datetime.now().date():
                    verified_team_list.append(team)
            context['verified_team_list'] = verified_team_list

        user_objects = User.objects.all()
        user_list = []
        amount_list = []


        limited_user_list = []
        limited_amount_list = []

        for user in user_objects:
            if not user.is_staff and user.backings:

                limited_backing = user.backings.filter(
                    created_at__lte=datetime.datetime.today(),
                    created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30),
                )


                limited_amount = limited_backing.aggregate(total_amount=Sum(F('amount')))
                if not limited_amount['total_amount']:
                    limited_amount['total_amount'] = 0
                limited_amount_list.append(limited_amount['total_amount'])
                
                backing_amount = user.backings.aggregate(total_amount=Sum(F('amount')))
                if backing_amount['total_amount'] == None:
                    backing_amount['total_amount'] = 0
                amount_list.append(backing_amount['total_amount'])
                user_list.append("{} {}".format(user.first_name, user.last_name[0]))

        limited_combined_list = zip(user_list, limited_amount_list)
        limited_all = sorted(limited_combined_list, key=lambda x: x[1], reverse=True)
        context['limited_user_list'] = limited_all

        combined_list = zip(user_list, amount_list)
        all = sorted(combined_list, key=lambda x: x[1], reverse=True)
        context['user_list'] = all


        return context


class ExploreView(generic.ListView):
    model = Team
    template_name = 'teams/explore.html'
    context_object_name = 'team_list'


class LoginSuccess(TemplateView):
    template_name = "registration/login-success.html"


class LogoutSuccess(TemplateView):
    template_name = "registration/logout-success.html"


class SignUpSuccess(TemplateView):
    template_name = "registration/signup-email-sent.html"


class ProjectCreationSuccess(TemplateView):
    template_name = "registration/project-inspect.html"


class LandPage(TemplateView):
    template_name = 'landing/landnew.html'


class FAQPage(TemplateView):
    template_name = 'faq.html'


class ContactPage(TemplateView):
    template_name = 'contact.html'


class TOSPage(TemplateView):
    template_name = 'tos.html'


class SubscribeSuccess(TemplateView):
    template_name = 'accounts/mailchimpsub/subscribe_success.html'


class UnSubscribeSuccess(TemplateView):
    template_name = 'accounts/mailchimpsub/unsubscribe_success.html'


class NotFoundPage(TemplateView):
    template_name = 'landing/404.html'


class ServerErrorPage(TemplateView):
    template_name = 'landing/500.html'


class EducatePage(TemplateView):
    template_name = 'landing/education.html'


class PrivacyPage(TemplateView):
    template_name = 'privacy.html'


class Handbook(TemplateView):
    template_name = 'creation-handbook.html'

