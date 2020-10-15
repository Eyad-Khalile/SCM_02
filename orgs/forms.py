from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _


# ============ User =============================
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,  required=True,
                             help_text=_('حقل إجباري, يرجى إدخال بريد إلكتروني صحيح لتتمكن من تفعيل حسابك'), label=_('عنوان بريد إلكتروني'))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class OrgProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=255, min_length=3, label=_('اسم المنظمة'),
                           help_text=_(
                               ''),
                           widget=forms.TextInput(
                               attrs={'placeholder': _('هذا الحقل لا يقبل الحروف الخاصه و الرموز')})
                           )
    name_en_ku = forms.CharField(max_length=255, min_length=3, required=False, label=_('اسم المنظمة باللغة الانكليزية أو الكردية'),
                                 widget=forms.TextInput(
        attrs={'placeholder': _('هذا الحقل لا يقبل الحروف الخاصه و الرموز')})
    )
    short_cut = forms.CharField(max_length=255, min_length=3, required=False, label=_('الاسم المختصر'),
                                widget=forms.TextInput(
        attrs={'placeholder': _('هذا الحقل لا يقبل الحروف الخاصه و الرموز')})
    )
    message = forms.CharField(max_length=2000, min_length=3, required=False, label="الرؤية و الرسالة", widget=forms.Textarea(
        attrs={'placeholder': 'هذا الحقل لا يقبل الحروف الخاصه و الرموز'}))

    name_managing_director = forms.CharField(max_length=255, min_length=3, required=False, label=_('اسم رئيس مجلس اﻹدارة'),
                                             widget=forms.TextInput(
        attrs={'placeholder': _('هذا الحقل لا يقبل الحروف الخاصه و الرموز')})
    )
    name_ceo = forms.CharField(max_length=255, min_length=3, required=False, label=_('اسم المدير التنفيذي'),
                               widget=forms.TextInput(
        attrs={'placeholder': _('هذا الحقل لا يقبل الحروف الخاصه و الرموز')})
    )
    site_web = forms.URLField(
        max_length=255, min_length=3, required=False, label=_('الموقع الالكتروني'), widget=forms.TextInput(attrs={'placeholder': "Ex: mysite.com"}))

    facebook = forms.URLField(
        max_length=255, min_length=3, required=False, label=_('صفحة فيسبوك'), widget=forms.TextInput(attrs={'placeholder': ""}))

    twitter = forms.URLField(
        max_length=255, min_length=3, required=False, label=_('صفحة تويتر'), widget=forms.TextInput(attrs={'placeholder': ""}))

    email = forms.EmailField(
        max_length=255, min_length=3, required=False, label=_('البريد الاكتروني'), widget=forms.TextInput(attrs={'placeholder': "Ex: myemail@example.com"}))

    name_person_contact = forms.CharField(max_length=255, min_length=3, required=False, label=_('اسم الشخص المسؤول عن التواصل'),
                                          widget=forms.TextInput(
        attrs={'placeholder': _('هذا الحقل لا يقبل الحروف الخاصه و الرموز')})
    )

    email_person_contact = forms.EmailField(
        max_length=255, min_length=3, required=False, label=_('البريد الاكتروني للشخص المسؤول عن التواصل'), widget=forms.TextInput(attrs={'placeholder': "Ex: email@example.com"}))

    org_adress = forms.CharField(max_length=255, min_length=3, label=_('عنوان المقر الرئيسي'),
                                 widget=forms.TextInput(
        attrs={'placeholder': _('هذا الحقل لا يقبل الحروف الخاصه و الرموز')})
    )
    coalition_name = forms.CharField(max_length=255, min_length=3, required=False, label=_('اسم الشبكة / التحالف'),
                                     widget=forms.TextInput(
        attrs={'placeholder': _('هذا الحقل لا يقبل الحروف الخاصه و الرموز')})
    )

    class Meta:
        model = OrgProfile
        fields = [
            'name',
            'name_en_ku',
            'short_cut',
            'org_type',
            'position_work',
            'city_work',
            'logo',
            'message',
            'name_managing_director',
            'name_ceo',
            'site_web',
            'facebook',
            'twitter',
            'email',
            'phone',
            'name_person_contact',
            'email_person_contact',
            'work_domain',
            'target_cat',
            'date_of_establishment',
            'is_org_registered',
            'org_registered_country',
            'org_adress',
            'org_members_count',
            'org_members_womans_count',
            'w_polic_regulations',
            'org_member_with',
            'coalition_name',
        ]


class OrgConfirmForm(forms.ModelForm):
    class Meta:
        model = OrgProfile
        fields = [
            'publish',
        ]


# ::::::::::::::::: ORGS NEWS :::::::::::::::::
class NewsForm(forms.ModelForm):

    class Meta:
        model = OrgNews
        fields = [
            'org_name',
            'title',
            'content',
            'image',
        ]


class NewsConfirmForm(forms.ModelForm):

    class Meta:
        model = OrgNews
        fields = [
            'publish',
        ]
