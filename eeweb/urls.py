
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordResetView, PasswordChangeView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.urls import path, include, re_path

from . import settings
from . import views


urlpatterns = [
   re_path(r'^hidden/admin/', admin.site.urls, name='admin'),
   re_path(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
   re_path(r'^$', views.IndexView.as_view(), name='home'),
   re_path(r'^transact/', include('transact.urls', namespace='transact')),
   re_path(r'^about/$', views.LandPage.as_view(), name='about'),
   re_path(r'^FAQ/$', views.FAQPage.as_view(), name='faq'),
   re_path(r'^TermsofService/$', views.TOSPage.as_view(), name='tos'),
   re_path(r'^pagenotfound/$', views.NotFoundPage.as_view(), name='404'),
   re_path(r'^server_error/$', views.ServerErrorPage.as_view(), name='500'),
   re_path(r'^educational_material/$', views.EducatePage.as_view(), name='educate'),
   re_path(r'^contact/$', views.ContactPage.as_view(), name='contact'),
   re_path(r'^privacy_policy/$', views.PrivacyPage.as_view(), name='privacy'),
   re_path(r'^back/', include('stripe_api.urls', 'stripe_api')),
   re_path(r'^teams/', include('teams.urls', namespace='teams')),
   re_path(r"^accounts/", include("accounts.urls", namespace="accounts")),
   re_path(r"^accounts/", include("django.contrib.auth.urls")),
   re_path(r'^accounts/', include("allauth.urls")),
   re_path(r'^accounts/password/reset/$', PasswordResetView,
        {'template_name': 'registration/password_reset_form.html',
                          'email_template_name': 'email/password_reset/password_reset.txt',
                                                 'html_email_template_name': 'email/password_reset/password_reset.html',
'subject_template_name': 'email/password_reset/password_reset_subject.txt'
}
, name='password_reset'),
   re_path(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordChangeView,
        {'template_name': 'registration/password_change.html'}, name='password_change'),
   re_path(r'^accounts/password/reset/done/$',
        PasswordResetDoneView,
        {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
   re_path(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView,
        {'template_name': 'registration/password_reset_confirm.html'},
        name='password_reset_confirm'),
   re_path(r'^accounts/password/done/$',
        PasswordResetCompleteView,
        {'template_name': 'registration/password_reset_complete.html'},
        name='password_reset_complete'),
   re_path(r'^signup/success/', views.SignUpSuccess.as_view(), name='signup_success'),
   re_path(r'^login/success/', views.LoginSuccess.as_view(), name='login_success'),
   re_path(r'^logout/success/', views.LogoutSuccess.as_view(), name='logout_success'),
   re_path(r'^subscribe_success/', views.SubscribeSuccess.as_view(), name='subscribe_success'),
   re_path(r'^unsubscribe_success/', views.UnSubscribeSuccess.as_view(), name='unsubscribe_success'),
   re_path(r'^project/creation/success/', views.ProjectCreationSuccess.as_view(), name='project_success'),
   re_path(r'^apply/', TemplateView.as_view(template_name="teams/fund_your_team.html"), name='apply'),
   re_path(r'^handbook/', views.Handbook.as_view(), name='handbook'),
]
urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
