# import phonenumbers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import *
from .models import *
from django.contrib import messages
from .tokens import account_activation_token
import os
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.core.mail import EmailMessage
from django.utils.timezone import datetime
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from .filters import *


# ::::::::::::: SIGNE UP :::::::::::::::


def signe_up(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        users = User.objects.all()
        emails = []
        for user in users:
            emails += user.email,

        if request.method == 'POST':
            form = SignUpForm(request.POST or None)
            user_email = request.POST.get('email')

            if user_email not in emails:
                if form.is_valid():
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()

                    current_site = get_current_site(request)
                    subject = 'Activate Your Account.'
                    message = render_to_string('register/account_activation_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(
                        subject, message, to=[to_email]
                    )
                    email.send()

                    username = form.cleaned_data.get('username')

                    messages.success(
                        request, f'Your Account has been created Successful with username ( {username} ) !, Please confirm your email address to complete the registration ')
                    return redirect('home')
            else:

                if user_email in emails:
                    messages.error(
                        request, f'Please Sign-up with another email address, this email ( {user_email} ) is already in use')
                    return redirect('signe_up')
                # else:

        else:
            form = SignUpForm()

        context = {
            'form': form
        }
        return render(request, 'register/signe-up.html', context)

# def signe_in(request):
#     return render(request, 'register/signe-in.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'register/active.html')


@login_required(login_url='signe_in')
def profile(request):

    if request.user.is_superuser:
        return redirect('profile_supper')

    if request.user.is_staff:
        return redirect('profile_staff')

    # profs = OrgProfile.objects.filter(user=request.user)
    profs = OrgProfile.objects.all().filter(user=request.user)

    for prof in profs:
        if prof and prof.user_id == request.user.id:
            org_type = prof.get_org_type_display()
            position_work = prof.get_position_work_display()
            city_work = prof.get_city_work_display()
            work_domain = prof.get_work_domain_display()
            target_cat = prof.get_target_cat_display()
            org_registered_country = prof.get_org_registered_country_display()
            w_polic_regulations = prof.get_w_polic_regulations_display()

            context = {
                'profs': profs,
                'org_type': org_type,
                'position_work': position_work,
                'city_work': city_work,
                'work_domain': work_domain,
                'target_cat': target_cat,
                'org_registered_country': org_registered_country,
                'w_polic_regulations': w_polic_regulations,
            }

        # else:

        #     context = {
        #         'profs': profs,
        #     }
            return render(request, 'profiles/profile.html', context)


@login_required(login_url='signe_in')
def admin_dashboard(request):

    if request.user.is_superuser:
        profs = OrgProfile.objects.all()

        for pro in profs:
            org_type = pro.get_org_type_display()
            position_work = pro.get_position_work_display()
            city_work = pro.get_city_work_display()
            work_domain = pro.get_work_domain_display()
            target_cat = pro.get_target_cat_display()
            org_registered_country = pro.get_org_registered_country_display()
            w_polic_regulations = pro.get_w_polic_regulations_display()

        context = {
            'profs': profs,
            'org_type': org_type,
            'position_work': position_work,
            'city_work': city_work,
            'work_domain': work_domain,
            'target_cat': target_cat,
            'org_registered_country': org_registered_country,
            'w_polic_regulations': w_polic_regulations,
        }
        return render(request, 'profiles/layout_profile.html', context)


@login_required(login_url='signe_in')
def orgs_orders_etude(request):
    orgs = OrgProfile.objects.filter(publish=False)

    myFilter = OrgsFilter(request.GET, queryset=orgs)
    orgs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(orgs, 12)
    page = request.GET.get('page')
    try:
        orgs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        orgs = paginator.page(paginator.num_pages)

    context = {
        'orgs': orgs,
        'myFilter': myFilter,
    }
    return render(request, 'profiles/orgs_orders_etude.html', context)


@login_required(login_url='signe_in')
def orgs_orders_published(request):
    orgs = OrgProfile.objects.filter(publish=True)

    myFilter = OrgsFilter(request.GET, queryset=orgs)
    orgs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(orgs, 12)
    page = request.GET.get('page')
    try:
        orgs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        orgs = paginator.page(paginator.num_pages)

    context = {
        'orgs': orgs,
        'myFilter': myFilter,
    }
    return render(request, 'profiles/orgs_orders_published.html', context)


@login_required(login_url='signe_in')
def profile_staff(request):
    if request.user.is_staff:
        profs = OrgProfile.objects.all()

        for pro in profs:
            org_type = pro.get_org_type_display()
            position_work = pro.get_position_work_display()
            city_work = pro.get_city_work_display()
            work_domain = pro.get_work_domain_display()
            target_cat = pro.get_target_cat_display()
            org_registered_country = pro.get_org_registered_country_display()
            w_polic_regulations = pro.get_w_polic_regulations_display()

        context = {
            'profs': profs,
            'org_type': org_type,
            'position_work': position_work,
            'city_work': city_work,
            'work_domain': work_domain,
            'target_cat': target_cat,
            'org_registered_country': org_registered_country,
            'w_polic_regulations': w_polic_regulations,
        }
        return render(request, 'profiles/staff_profile.html', context)
    else:
        return redirect('profile')


@login_required(login_url='signe_in')
def org_profile(request):
    if request.method == 'POST':
        form = OrgProfileForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()

            messages.success(
                request, 'لقد تم تسحيل بياناتكم بنجاح و ستتم دراستها باقرب وقت')
            return redirect('home')

    else:
        form = OrgProfileForm()

    context = {
        'form': form
    }
    return render(request, 'profiles/org_profile_form.html', context)


@login_required(login_url='signe_in')
def org_profile_edit(request, pk):
    org_prof = OrgProfile.objects.get(id=pk)

    if request.method == 'POST':
        form = OrgProfileForm(request.POST or None,
                              files=request.FILES, instance=org_prof)
        if form.is_valid():
            user = form.save(commit=False)
            user.updated_at = datetime.utcnow()
            user.save()

            messages.success(
                request, _('لقد تم تعديل الملف الشخصي بنجاح'))
            return redirect('profile')

    else:
        form = OrgProfileForm(instance=org_prof)

    context = {
        'form': form
    }
    return render(request, 'profiles/org_profile_update.html', context)


# =========== Page 404 ==================
def page_not_found_view(request, exception):
    return render(request, 'errors/404.html')


def home(request):
    orgs = OrgProfile.objects.filter(publish=True).order_by('published_at')

    # the 3 last prgs
    last = orgs.last()
    last_org = last.id
    av_last_org = last_org - 1
    av_av_last_org = av_last_org - 1

    print(last_org)
    print(av_last_org)
    print(av_av_last_org)

    context = {
        'orgs': orgs,
        'last_org': last_org,
        'av_last_org': av_last_org,
        'av_av_last_org': av_av_last_org,
    }
    return render(request, 'orgs/home.html', context)


# L'AFFICHAGE DES ORGS PUBLISHED
def guide(request):
    orgs = OrgProfile.objects.filter(publish=True).order_by('-created_at')

    myFilter = OrgsFilter(request.GET, queryset=orgs)
    orgs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(orgs, 12)
    page = request.GET.get('page')
    try:
        orgs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        orgs = paginator.page(paginator.num_pages)

    context = {
        'orgs': orgs,
        'myFilter': myFilter,
    }
    return render(request, 'orgs//guid/orgs_guide.html', context)


# L'AFFICHAGE DES ORGS NOT PUBLISHED
def guide_not_pub(request):
    orgs = OrgProfile.objects.filter(publish=False).order_by('-created_at')

    # PAGINATEUR
    paginator = Paginator(orgs, 12)
    page = request.GET.get('page')
    try:
        orgs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        orgs = paginator.page(paginator.num_pages)

    context = {
        'orgs': orgs,
    }
    return render(request, 'orgs/guid/orgs_guid_conf_pub.html', context)


# @register.filter(name='phonenumber')
# def phonenumber(value, country=None):
#     return phonenumbers.parse(value, country)


# ORG DETAIL تفاصيل المنظمة مع الموافقة و الرفض
def particip_detail(request, par_id):
    org = get_object_or_404(OrgProfile, id=par_id)

    org_type = org.get_org_type_display()
    position_work = org.get_position_work_display()
    city_work = org.get_city_work_display()
    work_domain = org.get_work_domain_display()
    target_cat = org.get_target_cat_display()
    org_registered_country = org.get_org_registered_country_display()
    w_polic_regulations = org.get_w_polic_regulations_display()

    if request.method == 'POST':
        print('request ======', request)
        form = OrgConfirmForm(request.POST or None, instance=org)
        if form.is_valid():
            pub = form.save(commit=False)
            pub.published_at = datetime.utcnow()
            pub.save()

            messages.success(request, _(
                'لقد تم تغيير حالة الطلب للمنظمة بنجاح'))

            # org_status = form.cleaned_data.get('publish')
            # if org_status == 'True':
            #     messages.success(request, _(
            #         'لقد تم قبول طلب تسجيل المنظمة بنجاح'))
            # if org_status == 'False':
            #     messages.info(request, _(
            #         'لقد تم رفض طلب تسجيل المنظمة بنجاح'))

            return redirect('guide')
    else:
        form = OrgConfirmForm(instance=org)

    context = {
        'org': org,
        'form': form,
        'org_type': org_type,
        'position_work': position_work,
        'city_work': city_work,
        'work_domain': work_domain,
        'target_cat': target_cat,
        'org_registered_country': org_registered_country,
        'w_polic_regulations': w_polic_regulations,
    }
    return render(request, 'profiles/particip_detail.html', context)


def guide_filter(request, work_id):
    id = work_id

    list_work = ''
    if id == '1':
        list_work = 'اﻹعلام'
    elif id == '2':
        list_work = 'التعليم'
    elif id == '3':
        list_work = 'الحماية'
    elif id == '4':
        list_work = 'سبل العيش و اﻷمن الغذائي'
    elif id == '5':
        list_work = 'مشاريع النظافة و المياه و الصرف الصحي'
    elif id == '6':
        list_work = 'التنمية'
    elif id == '7':
        list_work = 'القانون و مناصرة و سياسة'
    elif id == '8':
        list_work = 'المانحين و دعم العمل التطوعي'
    elif id == '9':
        list_work = 'المنظمات دينية'
    elif id == '10':
        list_work = 'التجمعات و الاتحادات المهنية'
    elif id == '11':
        list_work = 'الصحة'
    elif id == '12':
        list_work = 'الدراسات و اﻷبحاث'

    context = {
        'id': id,
        'list_work': list_work
    }
    return render(request, 'orgs/guid/orgs_guide_filter.html', context)


# أخبار المجتمع المدني
def news(request):
    return render(request, 'orgs/news/orgs_news.html')


# ORGS NEWS / NEWS PUBLISHED أخبار المنظمات
def orgs_news(request):
    news = OrgNews.objects.filter(publish=True).order_by('-created_at')

    myFilter = OrgsNewsFilter(request.GET, queryset=news)
    news = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(news, 12)
    page = request.GET.get('page')
    try:
        news = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        news = paginator.page(paginator.num_pages)

    context = {
        'news': news,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/news/orgs_news_news.html', context)


# ORGS ADD NEWS
@login_required(login_url='signe_in')
def orgs_add_news(request):

    if request.method == 'POST':
        form = NewsForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                user.org_name = org_name
            else:
                user.org_name = request.user
            user.save()

            messages.success(request, _(
                'لقد تمت إضافة الخبر بنجاح و ستتم دراسته قريباً'))

            return redirect('orgs_news')
    else:
        form = NewsForm()

    context = {
        'form': form,
    }
    return render(request, 'orgs/news/org_add_news.html', context)


# أخبار المنظمات قيد الدراسة
@login_required(login_url='signe_in')
def org_news_not_pub(request):
    news = OrgNews.objects.filter(publish=False).order_by('-created_at')

    # PAGINATEUR
    paginator = Paginator(news, 12)
    page = request.GET.get('page')
    try:
        news = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        news = paginator.page(paginator.num_pages)

    context = {
        'news': news,
    }
    return render(request, 'orgs/news/org_news_not_pub.html', context)


# ORG NEWS DETAIL
def news_detail(request, news_id):
    new = get_object_or_404(OrgNews, id=news_id)

    if request.method == 'POST':
        form = NewsConfirmForm(request.POST or None, instance=new)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تغيير حالة الخبر بنجاح'))
            return redirect('orgs_news')
    else:
        form = NewsConfirmForm(instance=new)

    context = {
        'new': new,
        'form': form,
    }
    return render(request, 'orgs/news/orgs_news_detail.html', context)


# NEWS EDIT
@login_required(login_url='signe_in')
def news_edit(request, news_id):
    new = get_object_or_404(OrgNews, id=news_id)

    if request.method == 'POST':
        form = NewsForm(request.POST or None,
                        files=request.FILES, instance=new)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل الخبر بنجاح'))
            return redirect('orgs_news')
    else:
        form = NewsForm(instance=new)

    context = {
        'new': new,
        'form': form,
    }
    return render(request, 'orgs/news/org_edit_news.html', context)

# :: NEWS DELETE ::


@login_required(login_url='signe_in')
def news_delete(request, news_id):
    new = get_object_or_404(OrgNews, id=news_id)

    if request.method == 'POST' and request.user.is_superuser:
        new.delete()

        messages.success(request, _(
            'لقد تم حذف الخبر بنجاح'))
        return redirect('orgs_news')

    context = {
        'new': new,
    }
    return render(request, 'orgs/news/org_news_delete.html', context)


# ::::::::::::: RAPPORT ::::::::::::::::::::::
@login_required(login_url='signe_in')
def add_rapport(request):

    if request.method == 'POST':
        form = RapportForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                user.org_name = org_name
            else:
                user.org_name = request.user
            user.save()

            messages.success(request, _(
                'لقد تمت إضافة التقرير بنجاح و ستتم دراسته قريباً'))

            return redirect('orgs_rapport')
    else:
        form = RapportForm()

    context = {
        "form": form,
    }
    return render(request, 'orgs/rapport/add_rapport.html', context)


# ::::::::: L'AFFICHAGE DES ORGS RAPPORTS ::::::::::::::::
def orgs_rapport(request):
    rapports = OrgRapport.objects.filter(publish=True).order_by('-created_at')

    myFilter = OrgsRapportFilter(request.GET, queryset=rapports)
    rapports = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(rapports, 12)
    page = request.GET.get('page')
    try:
        rapports = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        rapports = paginator.page(paginator.num_pages)

    context = {
        'rapports': rapports,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/rapport/rapport.html', context)


@login_required(login_url='signe_in')
def orgs_rapport_not_pub(request):
    rapports = OrgRapport.objects.filter(publish=False).order_by('-created_at')

    myFilter = OrgsRapportFilter(request.GET, queryset=rapports)
    rapports = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(rapports, 12)
    page = request.GET.get('page')
    try:
        rapports = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        rapports = paginator.page(paginator.num_pages)

    context = {
        'rapports': rapports,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/rapport/rapport_not_pub.html', context)


# RAPPORT DETAIL
def orgs_rapport_detail(request, rapport_id):
    rapport = get_object_or_404(OrgRapport, id=rapport_id)

    if request.method == 'POST':
        form = RapportConfirmForm(request.POST or None,
                                  files=request.FILES, instance=rapport)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل التقرير بنجاح'))
            return redirect('orgs_rapport')
    else:
        form = RapportConfirmForm(instance=rapport)

    context = {
        'rapport': rapport,
        'form': form,
    }
    return render(request, 'orgs/rapport/detail_rapport.html', context)


# DELETE RAPPORT
@login_required(login_url='signe_in')
def orgs_rapport_delete(request, rapport_id):
    rapport = get_object_or_404(OrgRapport, id=rapport_id)

    if request.method == 'POST' and request.user.is_superuser:
        rapport.delete()

        messages.success(request, _(
            'لقد تم حذف التقرري بنجاح'))
        return redirect('orgs_rapport')

    context = {
        'rapport': rapport,
    }
    return render(request, 'orgs/rapport/delete_rapport.html', context)


# UPDATE RAPPORT
@login_required(login_url='signe_in')
def edit_rapport(request, rapport_id):
    rapport = get_object_or_404(OrgRapport, id=rapport_id)

    if request.method == 'POST':
        form = RapportForm(request.POST or None,
                           files=request.FILES, instance=rapport)
        if form.is_valid():
            user = form.save(commit=False)
            user.updated_at = datetime.utcnow()
            user.save()

            messages.success(request, _(
                'لقد تمت تعديل التقرير بنجاح'))

            return redirect('orgs_rapport')
    else:
        form = RapportForm(instance=rapport)

    context = {
        "rapport": rapport,
        "form": form,
    }
    return render(request, 'orgs/rapport/edit_rapport.html', context)


# ::::::::::: DATA :::::::::::::::
# DATA PUB
def data(request):
    datas = OrgData.objects.filter(publish=True).order_by('-created_at')

    myFilter = OrgsDataFilter(request.GET, queryset=datas)
    datas = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(datas, 12)
    page = request.GET.get('page')
    try:
        datas = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        datas = paginator.page(paginator.num_pages)

    context = {
        'datas': datas,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/data/data.html', context)


@login_required(login_url='signe_in')
def add_data(request):
    if request.method == 'POST':
        form = DataForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                user.org_name = org_name
            else:
                user.org_name = request.user
            user.save()

            messages.success(request, _(
                'لقد تمت إضافة التقرير بنجاح و ستتم دراسته قريباً'))

            return redirect('data')
    else:
        form = DataForm()
    context = {
        'form': form,
    }

    return render(request, 'orgs/data/add_data.html', context)


def data_detail(request, data_id):
    data = get_object_or_404(OrgData, id=data_id)

    if request.method == 'POST':
        form = DataConfirmForm(request.POST or None,
                               files=request.FILES, instance=data)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل حالة البيان بنجاح'))
            return redirect('data')

    else:
        form = DataConfirmForm(instance=data)

    context = {
        'data': data,
        'form': form,
    }
    return render(request, 'orgs/data/detail_data.html', context)


@login_required(login_url='signe_in')
def data_not_pub(request):
    datas = OrgData.objects.filter(publish=False).order_by('-created_at')

    myFilter = OrgsDataFilter(request.GET, queryset=datas)
    datas = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(datas, 12)
    page = request.GET.get('page')
    try:
        datas = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        datas = paginator.page(paginator.num_pages)

    context = {
        'datas': datas,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/data/data_not_pub.html', context)


@login_required(login_url='signe_in')
def edit_data(request, data_id):
    data = get_object_or_404(OrgData, id=data_id)

    if request.method == 'POST':
        form = DataForm(request.POST or None,
                        files=request.FILES, instance=data)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل البيان بنجاح'))
            return redirect('data')

    else:
        form = DataForm(instance=data)

    context = {
        'form': form,
    }
    return render(request, 'orgs/data/edit_data.html', context)


@login_required(login_url='signe_in')
def delete_data(request, data_id):
    data = get_object_or_404(OrgData, id=data_id)
    if request.method == 'POST' and request.user.is_superuser:
        data.delete()

        messages.success(request, _(
            'لقد تم حذف البيان بنجاح'))
        return redirect('data')
    context = {
        'data': data,
    }
    return render(request, 'orgs/data/delete_data.html', context)


# :::::::::: MEDIA :::::::::::::::
def media(request):
    medias = OrgMedia.objects.filter(publish=True).order_by('-created_at')

    myFilter = OrgsMediaFilter(request.GET, queryset=medias)
    medias = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(medias, 12)
    page = request.GET.get('page')
    try:
        medias = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        medias = paginator.page(paginator.num_pages)

    context = {
        'medias': medias,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/media/media.html', context)


def add_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            org_name = form.cleaned_data.get('org_name')
            if org_name:
                user.org_name = org_name
            else:
                user.org_name = request.user
            user.save()

            messages.success(request, _(
                'لقد تمت إضافة المحتوى بنجاح و ستتم دراسته قريباً'))

            return redirect('media')
    else:
        form = MediaForm()

    context = {
        'form': form,
    }

    return render(request, 'orgs/media/add_media.html', context)


def media_detail(request, media_id):
    media = get_object_or_404(OrgMedia, id=media_id)

    if request.method == 'POST':
        form = MediaConfirmForm(request.POST or None,
                                files=request.FILES, instance=media)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل حالة المحتوى بنجاح'))
            return redirect('media')

    else:
        form = MediaConfirmForm(instance=media)

    context = {
        'media': media,
        'form': form,
    }
    return render(request, 'orgs/media/media_detail.html', context)


def media_not_pub(request):
    medias = OrgMedia.objects.filter(publish=False).order_by('-created_at')

    myFilter = OrgsMediaFilter(request.GET, queryset=medias)
    medias = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(medias, 12)
    page = request.GET.get('page')
    try:
        medias = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        medias = paginator.page(paginator.num_pages)

    context = {
        'medias': medias,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/media/media_not_pub.html', context)


def edit_media(request, media_id):
    media = get_object_or_404(OrgMedia, id=media_id)

    if request.method == 'POST':
        form = MediaForm(request.POST or None,
                         files=request.FILES, instance=media)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل المحتوى بنجاح'))
            return redirect('media')

    else:
        form = MediaForm(instance=media)

    context = {
        'media': media,
        'form': form,
    }
    return render(request, 'orgs/media/edit_media.html', context)


def delete_media(request, media_id):
    media = get_object_or_404(OrgMedia, id=media_id)
    if request.method == 'POST' and request.user.is_superuser:
        media.delete()

        messages.success(request, _(
            'لقد تم حذف المحتوى بنجاح'))
        return redirect('media')
    context = {
        'media': media,
    }
    return render(request, 'orgs/media/delete_media.html', context)


# RESEARCH
def research(request):
    return render(request, 'orgs/research/orgs_research.html')


def research_detail(request, res_id):
    id = res_id
    context = {
        'id': id,
    }
    return render(request, 'orgs/research/orgs_research_detail.html', context)


# RECOURCE

def resource(request):
    return render(request, 'orgs/resource/resource.html')


def resource_work(request):
    return render(request, 'orgs/resource/resource_work.html')


def resource_work_detail(request, work_id):
    id = work_id
    context = {
        'id': id,
    }
    return render(request, 'orgs/resource/resource_work_detail.html', context)


def resource_finance(request):
    return render(request, 'orgs/resource/resource_finance.html')


def resource_finance_perso(request):
    return render(request, 'orgs/resource/resource_finance_perso.html')


def resource_finance_perso_detail(request, id):
    id = id
    context = {
        'id': id,
    }
    # 6
    return render(request, 'orgs/resource/resource_finance_perso_detail.html', context)


def resource_finance_orgs(request):
    return render(request, 'orgs/resource/resource_finance_orgs.html')


def resource_finance_orgs_detail(request, id):
    id = id
    context = {
        'id': id,
    }
    # 8
    return render(request, 'orgs/resource/resource_finance_orgs_detail.html', context)


def resource_stectur(request):
    return render(request, 'orgs/resource/resource_strectur.html')


def resource_stectur_detail(request, id):
    id = id
    context = {
        'id': id,
    }
    # 10
    return render(request, 'orgs/resource/resource_strectur_detail.html', context)


def resource_upgrade(request):
    return render(request, 'orgs/resource/resource_upgrade.html')


def resource_upgrade_detail(request, id):
    id = id
    context = {
        'id': id,
    }
    # 12
    return render(request, 'orgs/resource/resource_upgrade_detail.html', context)


# CENTRE NEWS
def centre_news(request):
    return render(request, 'orgs/centre_news.html')


def centre_news_detail(request, id):
    id = id

    context = {
        'id': id,
    }
    return render(request, 'orgs/centre_news_detail.html', context)


# SITE POLITIQUE
def site_politic(request):
    return render(request, 'orgs/politic.html')


# CONTACT-US
# def contact(request):
#     return render(request, 'contact/contact.html')
