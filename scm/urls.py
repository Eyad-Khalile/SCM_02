"""scm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from orgs import views as orgs_views
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# urlpatterns = [
#     path('i18n/', include('django.conf.urls.i18n')),
#     path('admin/', admin.site.urls),
#     path('', include('orgs.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

favicon_view = RedirectView.as_view(url='static/favicon.ico',
                                    permanent=False)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path(_('admin'), admin.site.urls),
    path('', include('orgs.urls')),
    path('favicon.ico', favicon_view),
    prefix_default_language=False,
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)

handler404 = 'orgs.views.page_not_found_view'
# handler500 = 'article.views.page_not_found_view'
