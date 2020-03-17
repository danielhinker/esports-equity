from django.conf.urls import url

from . import views

app_name = 'accounts'

urlpatterns = [
    url(r"login/$", views.LoginView.as_view(), name="login"),
    url(r"logout/$", views.LogoutView.as_view(), name="logout"),
    url(r"signup/$", views.SignUp.as_view(), name="signup"),
    url(r'^profile/user/(?P<profile_pk>\d+)/$', views.ProfilePage, name="profile"),
    url(r'^profile/settings/$', views.ProfileSettings.as_view(), name='profile_settings'),
    url(r'^profile/dashboard/$', views.change_password, name='profile_dashboard'),
    url(r'mailsub/$', views.MailchimpSubscribe, name='subscribe'),
    url(r'mailunsub/$', views.MailchimpUnsubscribe, name='unsubscribe'),
    url(r'profile/settings/changename$', views.NameChangeSettings.as_view(), name='change_name'),
    url(r'profile/settings/changedescription$', views.DescriptionChangeSettings.as_view(), name='change_description'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^demolish/$', views.AccountDelete.as_view(), name='delete_account'),
    url(r'project/update/0048(?P<project_pk>\d+)/step/2$', views.ProjectCreateView2.as_view(), name='create_project_2'),
    url(r'project/update/0048(?P<project_pk>\d+)/step/3$', views.ProjectCreateView3.as_view(), name='create_project_3'),
    url(r'project/update/0048(?P<project_pk>\d+)/step/4$', views.RewardsCreate, name='create_project_4'),
    url(r'project/update/0032(?P<project_pk>\d+)/step/5$', views.ProjectCreateView5.as_view(), name='create_project_5'),
    url(r'project/update/0048(?P<project_pk>\d+)/step/6$', views.ProjectCreateView6.as_view(), name='create_project_6'),
    url(r'project/delete/0013(?P<project_pk>\d+)$', views.ProjectDeleteView.as_view(), name='delete_project'),
    url(r'^activate/(?P<key>.+)$', views.activation, name='activation'),
    url(r'^new-activation-link/$', views.new_activation_link, name='activation_link'),
]
