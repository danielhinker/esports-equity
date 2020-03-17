from django.conf.urls import url
from . import views

app_name = 'teams'
urlpatterns = [
    url(r'^all/$', views.ExploreView.as_view(), name='explore'),
    url(r'^details/(?P<team_id>\d+)/$', views.DetailTeam, name='detail'),
    url(r'^details/(?P<team_id>\d+)/follow/$',views.follow_team, name='follow'),
    url(r'^details/(?P<team_id>\d+)/unfollow/$', views.unfollow_team, name='unfollow'),
    url(r'^followed/$', views.all_follow, name='allfollowed'),
    url(r'apply/project/creation/step/1$', views.ProjectCreateView.as_view(), name='create_project'),
    url(r'apply/project/creation/0048(?P<project_pk>\d+)/step/2$', views.ProjectCreateView2.as_view(), name='create_project_2'),
    url(r'apply/project/creation/0048(?P<project_pk>\d+)/step/3$', views.ProjectCreateView3.as_view(), name='create_project_3'),
    url(r'apply/project/view/0048(?P<project_pk>\d+)/(?P<reward_pk>\d+)/step/4$', views.RewardsDeleteView4.as_view(), name='delete_reward'),
    url(r'apply/project/view/0048(?P<project_pk>\d+)/step/4$', views.RewardsDeleteAllView4.as_view(), name='delete_rewards_all'),
    url(r'apply/project/creation/0048(?P<project_pk>\d+)/step/4$', views.RewardsCreate, name='create_project_4'),
    url(r'apply/project/creation/0032(?P<project_pk>\d+)/step/5$', views.ProjectCreateView5.as_view(), name='create_project_5'),
    url(r'apply/project/creation/0048(?P<project_pk>\d+)/step/6$', views.ProjectCreateView6.as_view(), name='create_project_6'),
    url(r'apply/project/creation/success$', views.ProjectSuccessView7.as_view(), name='create_project_success'),
    url(r'apply/project/delete/0013(?P<project_pk>\d+)$', views.ProjectDeleteView.as_view(), name='delete_project'),
    url(r'back/project/0068(?P<project_pk>\d+)/step/1$', views.BackView, name='back_team'),
]

