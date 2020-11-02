from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _

# Register your models here.
# ::::::::::::: CONF ADMIN PAGE TITLE ::::::::::::::
admin.site.site_header = _('إدارة موقع SCM ')
admin.site.site_title = _('إدارة موقع SCM ')


admin.site.register(Profile)
admin.site.register(NewsLetter)
