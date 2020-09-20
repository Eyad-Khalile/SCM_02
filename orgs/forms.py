from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# ============ User =============================
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,  required=True,
                             help_text='حقل إجباري, يرجى إدخال بريد إلكتروني صحيح لتتمكن من تفعيل حسابك', label='عنوان بريد إلكتروني')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class OrgProfileForm(forms.ModelForm):
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
