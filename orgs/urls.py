from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # HOME AND LEGALE
    path('', views.home, name="home"),
    path('site_politic/', views.site_politic, name="site_politic"),

    # ORGS GUIDE
    path('guide/', views.guide, name="guide"),
    path('guide_conf/', views.guide_not_pub, name="guide_conf"),
    path('guide_filter/<str:work_id>', views.guide_filter, name="guide_filter"),

    # ORGS NEWS
    path('news/', views.news, name="news"),
    path('orgs_news/', views.orgs_news, name="orgs_news"),
    path('orgs_add_news/', views.orgs_add_news, name="orgs_add_news"),
    path('news_detail/<str:news_id>', views.news_detail, name="news_detail"),
    path('news_edit/<str:news_id>', views.news_edit, name="news_edit"),
    path('news_delete/<str:news_id>', views.news_delete, name="news_delete"),
    path('org_news_not_pub/', views.org_news_not_pub, name="org_news_not_pub"),

    # ORGS RAPPORT
    path('add_rapport/', views.add_rapport, name="add_rapport"),
    path('orgs_rapport/', views.orgs_rapport, name="orgs_rapport"),
    path('orgs_rapport_detail/<str:rapport_id>',
         views.orgs_rapport_detail, name="orgs_rapport_detail"),
    path('edit_rapport/<str:rapport_id>',
         views.edit_rapport, name="edit_rapport"),
    path('orgs_rapport_delete/<str:rapport_id>',
         views.orgs_rapport_delete, name="orgs_rapport_delete"),
    path('orgs_rapport_not_pub/', views.orgs_rapport_not_pub,
         name="orgs_rapport_not_pub"),

    # ORGS DATA
    path('data/', views.data, name="data"),
    path('add_data/', views.add_data, name="add_data"),
    path('data_detail/<str:data_id>', views.data_detail, name="data_detail"),
    path('edit_data/<str:data_id>', views.edit_data, name="edit_data"),
    path('delete_data/<str:data_id>', views.delete_data, name="delete_data"),
    path('data_not_pub/', views.data_not_pub, name="data_not_pub"),

    # ORGS MEDIA
    path('media/', views.media, name="media"),
    path('add_media/', views.add_media, name="add_media"),
    path('media_detail/<str:media_id>', views.media_detail, name="media_detail"),
    path('edit_media/<str:media_id>', views.edit_media, name="edit_media"),
    path('delete_media/<str:media_id>', views.delete_media, name="delete_media"),
    path('media_not_pub/', views.media_not_pub, name="media_not_pub"),

    # ORGS RESEARCH
    path('research/', views.research, name="research"),
    path('add_research/', views.add_research, name="add_research"),
    path('research_detail/<str:research_id>',
         views.research_detail, name="research_detail"),
    path('edit_research/<str:research_id>',
         views.edit_research, name="edit_research"),
    path('delete_research/<str:research_id>',
         views.delete_research, name="delete_research"),
    path('research_not_pub/', views.research_not_pub, name="research_not_pub"),

    # RECOURCE
    path('resource/', views.resource, name="resource"),
    path('resource_work/', views.resource_work, name="resource_work"),
    path('resource_work_detail/<str:work_id>',
         views.resource_work_detail, name="resource_work_detail"),
    path('resource_finance/', views.resource_finance, name="resource_finance"),
    path('resource_finance_perso/', views.resource_finance_perso,
         name="resource_finance_perso"),
    path('resource_finance_perso_detail/<str:id>',
         views.resource_finance_perso_detail, name="resource_finance_perso_detail"),
    path('resource_finance_orgs/', views.resource_finance_orgs,
         name="resource_finance_orgs"),
    path('resource_finance_orgs_detail/<str:id>',
         views.resource_finance_orgs_detail, name="resource_finance_orgs_detail"),
    path('resource_stectur/', views.resource_stectur, name="resource_stectur"),
    path('resource_stectur_detail/<str:id>',
         views.resource_stectur_detail, name="resource_stectur_detail"),
    path('resource_upgrade/', views.resource_upgrade, name="resource_upgrade"),
    path('resource_upgrade_detail/<str:id>',
         views.resource_upgrade_detail, name="resource_upgrade_detail"),

    # CENTRE NEWS
    path('centre_news/', views.centre_news, name="centre_news"),
    path('centre_news_detail/<str:id>',
         views.centre_news_detail, name="centre_news_detail"),

    # CONTACT-US
    # path('contact', views.contact, name="contact"),


    # SIGNE-IN AND SIGNE-UP
    # path('signe_in', views.signe_in, name="signe_in"),
    path('login/', auth_views.LoginView.as_view(template_name='register/signe-in.html'), name='signe_in'),
    path('signe_up/', views.signe_up, name="signe_up"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.activate, name='activate'),
    path('logout/', auth_views.LogoutView.as_view(template_name='register/logged_out.html'), name='logout'),
    path('profile/', views.profile, name="profile"),
    path('profile_supper/', views.admin_dashboard, name="profile_supper"),
    path('profile_staff/', views.profile_staff, name="profile_staff"),

    # Org Fill the form
    path('org_profile/', views.org_profile, name='org_profile'),
    # Org Edit the form
    path('org_profile_edit/<str:pk>',
         views.org_profile_edit, name='org_profile_edit'),
    path('orgs_orders_etude/', views.orgs_orders_etude, name='orgs_orders_etude'),
    path('orgs_orders_published/', views.orgs_orders_published,
         name='orgs_orders_published'),
    path('particip_detail/<str:par_id>',
         views.particip_detail, name="particip_detail"),

    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='register/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='register/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='register/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='register/password_reset_complete.html'), name='password_reset_complete'),

    # Password Change
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='register/password_change_done.html'), name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='register/password_change.html'), name='password_change'),
]
