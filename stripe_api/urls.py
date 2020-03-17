from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


from . import views

app_name = 'stripe_api'

urlpatterns = [
    url(r'start/(?P<project_pk>\d+)/$', views.stripe_page, name="back_team"),
    url(r'charge/information/', views.stripe_charge_2, name='back_team_2'),
    url(r'charge/complete/$', views.stripe_charge_3, name='back_team_3'),
    url(r'charge/success/$', views.BackSuccess.as_view(), name='back_success'),
    url(r'charge/page/(?P<project_pk>\d+)$', views.BackPage, name='back_page'),
    url(r'charge/page-2/(?P<project_pk>\d+)$', views.BackPage2, name='back_page_2'),
]