from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # HOME AND LEGALE
    path('', views.home, name="home"),
    path('site_politic', views.site_politic, name="site_politic"),

    # ORGS GUIDE
    path('guide', views.guide, name="guide"),
    path('guide_filter/<str:work_id>', views.guide_filter, name="guide_filter"),

    # ORGS NEWS
    path('news', views.news, name="news"),
    path('orgs_news', views.orgs_news, name="orgs_news"),
    path('news_detail/<str:news_id>', views.news_detail, name="news_detail"),
    path('orgs_rapport', views.orgs_rapport, name="orgs_rapport"),
    path('orgs_rapport_detail/<str:rapport_id>',
         views.orgs_rapport_detail, name="orgs_rapport_detail"),
    path('data', views.data, name="data"),
    path('data_detail/<str:data_id>', views.data_detail, name="data_detail"),
    path('media', views.media, name="media"),
    path('media_detail/<str:media_id>', views.media_detail, name="media_detail"),
    path('research', views.research, name="research"),
    path('research_detail/<str:res_id>',
         views.research_detail, name="research_detail"),

    # RECOURCE
    path('resource', views.resource, name="resource"),
    path('resource_work', views.resource_work, name="resource_work"),
    path('resource_work_detail/<str:work_id>',
         views.resource_work_detail, name="resource_work_detail"),
    path('resource_finance', views.resource_finance, name="resource_finance"),
    path('resource_finance_perso', views.resource_finance_perso,
         name="resource_finance_perso"),
    path('resource_finance_perso_detail/<str:id>',
         views.resource_finance_perso_detail, name="resource_finance_perso_detail"),
    path('resource_finance_orgs', views.resource_finance_orgs,
         name="resource_finance_orgs"),
    path('resource_finance_orgs_detail/<str:id>',
         views.resource_finance_orgs_detail, name="resource_finance_orgs_detail"),
    path('resource_stectur', views.resource_stectur, name="resource_stectur"),
    path('resource_stectur_detail/<str:id>',
         views.resource_stectur_detail, name="resource_stectur_detail"),
    path('resource_upgrade', views.resource_upgrade, name="resource_upgrade"),
    path('resource_upgrade_detail/<str:id>',
         views.resource_upgrade_detail, name="resource_upgrade_detail"),

    # CENTRE NEWS
    path('centre_news', views.centre_news, name="centre_news"),
    path('centre_news_detail/<str:id>',
         views.centre_news_detail, name="centre_news_detail"),

    # CONTACT-US
    # path('contact', views.contact, name="contact"),


    # SIGNE-IN AND SIGNE-UP
    # path('signe_in', views.signe_in, name="signe_in"),
    path('login/', auth_views.LoginView.as_view(template_name='register/signe-in.html'), name='signe_in'),
    path('signe_up', views.signe_up, name="signe_up"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.activate, name='activate'),
    path('logout/', auth_views.LogoutView.as_view(template_name='register/logged_out.html'), name='logout'),
    path('profile/', views.profile, name="profile"),
    path('org_profile/', views.org_profile, name='org_profile'),
    path('org_profile_edit/<str:pk>',
         views.org_profile_edit, name='org_profile_edit'),
    path('particip_detail/<str:par_id>',
         views.particip_detail, name="particip_detail"),
]
