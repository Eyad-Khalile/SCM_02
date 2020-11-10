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
import traceback
from django.db.models import Q


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

                    # messages.success(
                    #     request, f'Your Account has been created Successful with username ( {username} ) !, Please confirm your email address to complete the registration ')
                    messages.success(
                        request, _(f'تم إنشاء حسابك بنجاح باسم المستخدم ( {username} ) !, يرجى تأكيد عنوان بريدك الإلكتروني لإكمال التسجيل '))
                    return redirect('home')
            else:

                if user_email in emails:
                    # messages.error(
                    #     request, f'Please Sign-up with another email address, this email ( {user_email} ) is already in use')
                    messages.error(
                        request, _(f'يرجى التسجيل باستخدام عنوان بريد إلكتروني آخر، هذا البريد الإلكتروني ( {user_email} ) مستخدم مسبقاً'))
                    return redirect('signe_up')
                # else:

        else:
            form = SignUpForm()

        context = {
            'form': form
        }
        return render(request, 'register/signe-up.html', context)


# ACTIVATION ACCOUNT


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


# CITYES
@login_required(login_url='signe_in')
def add_city(request):

    if request.method == 'POST':
        form = CityForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = CityForm()

            messages.success(
                request, 'لقد تمت إضافة المحافظة بنجاح')

            # return redirect('city')
    else:
        form = CityForm()

    context = {
        'form': form
    }
    return render(request, 'city/add_city.html', context)


@login_required(login_url='signe_in')
def edit_city(request, city_id):
    city = get_object_or_404(City, id=city_id)

    if request.method == 'POST':
        form = CityForm(request.POST or None, instance=city)
        if form.is_valid():
            date = form.save(commit=False)
            date.updated_at = datetime.utcnow()
            date.save()

            form = CityForm()

            messages.success(
                request, 'لقد تمت تعديل المحافظة بنجاح')

            # return redirect('city')

    else:
        form = CityForm(instance=city)

    context = {
        'city': city,
        'form': form
    }
    return render(request, 'city/edite_city.html', context)


@login_required(login_url='signe_in')
def delete_city(request, city_id):
    city = get_object_or_404(City, id=city_id)

    if request.method == 'POST' and request.user.is_superuser:
        city.delete()

        messages.success(request, _(
            'لقد تم حذف المحافظه بنجاح'))
        return redirect('city')

    context = {
        'city': city,
    }
    return render(request, 'city/delete_city.html', context)


@login_required(login_url='signe_in')
def view_city(request):
    cityes = City.objects.all().order_by('id')

    context = {
        'cityes': cityes,
    }
    return render(request, 'city/view_city.html', context)


# AJAX
def load_cities(request):
    position_work = request.GET.get('position_work')
    cities = City.objects.filter(position_work=position_work).all()
    return render(request, 'city/city_dropdown_list_options.html', {'cities': cities})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


# PROFILE
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
            #city_work = prof.get_city_work_display()
            work_domain = prof.get_work_domain_display()
            target_cat = prof.get_target_cat_display()
            org_registered_country = prof.get_org_registered_country_display()
            w_polic_regulations = prof.get_w_polic_regulations_display()

            context = {
                'profs': profs,
                'org_type': org_type,
                'position_work': position_work,
                # 'city_work': city_work,
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
        count_orgs = OrgProfile.objects.all().count()
        profs = OrgProfile.objects.all()

        for pro in profs:
            org_type = pro.get_org_type_display()
            position_work = pro.get_position_work_display()
            # city_work = pro.get_city_work_display()
            work_domain = pro.get_work_domain_display()
            target_cat = pro.get_target_cat_display()
            org_registered_country = pro.get_org_registered_country_display()
            w_polic_regulations = pro.get_w_polic_regulations_display()

        context = {
            'profs': profs,
            'org_type': org_type,
            'position_work': position_work,
            # 'city_work': city_work,
            'work_domain': work_domain,
            'target_cat': target_cat,
            'org_registered_country': org_registered_country,
            'w_polic_regulations': w_polic_regulations,
            'count_orgs': count_orgs
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
            #city_work = pro.get_city_work_display()
            work_domain = pro.get_work_domain_display()
            target_cat = pro.get_target_cat_display()
            org_registered_country = pro.get_org_registered_country_display()
            w_polic_regulations = pro.get_w_polic_regulations_display()

        context = {
            'profs': profs,
            'org_type': org_type,
            'position_work': position_work,
            # 'city_work': city_work,
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
            prof = form.save(commit=False)
            user = form.cleaned_data.get('user')
            if user:
                prof.user = user
            else:
                prof.user = request.user
            prof.save()

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


@login_required(login_url='signe_in')
def org_profile_delete(request, pk):
    org_prof = OrgProfile.objects.get(id=pk)

    if request.method == 'POST' and request.user.is_superuser:
        org_prof.delete()

        messages.success(request, _(
            'لقد تم حذف الملف بنجاح'))
        return redirect('home')

    context = {
        'org_prof': org_prof,
    }
    return render(request, 'profiles/org_profile_delete.html', context)


# =========== Page 404 ==================
def page_not_found_view(request, exception):
    return render(request, 'errors/404.html')


# NEWS LETTER
# def NewsLetter(request):
#     if request.is_ajax():
#         formNews = NewsLetterForm(request.POST or None)
#         if formNews.is_valid():
#             formNews.save()
#             # formNews = NewsLetterForm()
#             return JsonResponse({
#                 'msg': 'Success',
#             }, status=200)

#             messages.success(request, _(
#                 'لقد تم طلب الاشتراك بآخر اﻷخبار بنجاح'))

#     else:
#         formNews = NewsLetterForm()
#     context = {
#         'formNews': formNews,
#     }

#     return render(request, 'combonents/footer.html', context)


# HOME PAGE
def home(request):
    orgs = OrgProfile.objects.filter(publish=True).order_by('-published_at')
    news = OrgNews.objects.filter(publish=True).order_by('-published_at')
    jobs = OrgJob.objects.filter(publish=True).order_by('-published_at')
    capacites = OrgCapacityOpp.objects.filter(
        publish=True).order_by('-published_at')

    # the Last orgs
    if orgs.first():
        first_org = orgs.first().id
    else:
        first_org = _('لا يوجد حاليا منظمات')

    # the Last news
    if news.first():
        first_news = news.first().id
    else:
        first_news = _('لا يوجد حالي أخبار')

    # the Last job
    if jobs.first():
        first_job = jobs.first().id
    else:
        first_job = _('لا يوجد')

    # the Last job
    if capacites.first():
        first_capacity = capacites.first().id
    else:
        first_capacity = _('لا يوجد حاليا فرص بناء')

    # if request.is_ajax():
    if request.method == 'POST':
        formNews = NewsLetterForm(request.POST or None)
        if formNews.is_valid():
            formNews.save()
            formNews = NewsLetterForm()

            messages.success(request, _(
                'لقد تم طلب الاشتراك بآخر اﻷخبار بنجاح'))

            # return JsonResponse({
            #     'msg': 'Success',
            # }, status=200)

        else:
            messages.error(request, _(
                'هذا البريد الالكتروني موجود مسبقاً يرجى التسجيل ببريد الكتروني أخر'))

    else:
        formNews = NewsLetterForm()

    context = {
        'orgs': orgs,
        'first_org': first_org,
        'news': news,
        'first_news': first_news,
        'jobs': jobs,
        'first_job': first_job,
        'capacites': capacites,
        'first_capacity': first_capacity,
        'formNews': formNews,
    }
    return render(request, 'orgs/home.html', context)


# L'AFFICHAGE DES ORGS PUBLISHED
def guide(request):
    orgs = OrgProfile.objects.filter(publish=True).order_by('-published_at')

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
    # city_work = org.()
    work_domain = org.get_work_domain_display()
    target_cat = org.get_target_cat_display()
    org_registered_country = org.get_org_registered_country_display()
    w_polic_regulations = org.get_w_polic_regulations_display()

    if request.method == 'POST':
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
        # 'city_work': city_work,
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
    news = OrgNews.objects.filter(Q(publish=True) & ~Q(
        org_name__name='khalil')).order_by('-created_at')

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
    news = OrgNews.objects.filter(publish=True).order_by('-created_at')

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
        'news': news,
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
                'لقد تم تعديل حالة التقرير بنجاح'))
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
            'لقد تم حذف التقرير بنجاح'))
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
                'لقد تمت إضافة البيان بنجاح و ستتم دراسته قريباً'))

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


@login_required(login_url='signe_in')
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


@login_required(login_url='signe_in')
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


@login_required(login_url='signe_in')
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


@login_required(login_url='signe_in')
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
    researchs = OrgResearch.objects.filter(
        publish=True).order_by('-created_at')

    myFilter = OrgsResearchFilter(request.GET, queryset=researchs)
    researchs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(researchs, 12)
    page = request.GET.get('page')
    try:
        researchs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        researchs = paginator.page(paginator.num_pages)

    context = {
        'researchs': researchs,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/research/research.html', context)


@login_required(login_url='signe_in')
def add_research(request):
    if request.method == 'POST':
        form = ResearchForm(request.POST or None, files=request.FILES)
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
                'لقد تمت إضافة البحث بنجاح و ستتم دراسته قريباً'))

            return redirect('research')
    else:
        form = ResearchForm()

    context = {
        'form': form,
    }

    return render(request, 'orgs/research/add_research.html', context)


def research_detail(request, research_id):
    research = get_object_or_404(OrgResearch, id=research_id)

    if request.method == 'POST':
        form = ResearchConfirmForm(request.POST or None,
                                   files=request.FILES, instance=research)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل حالة البحث بنجاح'))
            return redirect('research')

    else:
        form = ResearchConfirmForm(instance=research)

    context = {
        'research': research,
        'form': form,
    }
    return render(request, 'orgs/research/detail_research.html', context)


@login_required(login_url='signe_in')
def research_not_pub(request):
    researchs = OrgResearch.objects.filter(
        publish=False).order_by('-created_at')

    myFilter = OrgsResearchFilter(request.GET, queryset=researchs)
    researchs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(researchs, 12)
    page = request.GET.get('page')
    try:
        researchs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        researchs = paginator.page(paginator.num_pages)

    context = {
        'researchs': researchs,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/research/research_not_pub.html', context)


@login_required(login_url='signe_in')
def edit_research(request, research_id):
    research = get_object_or_404(OrgResearch, id=research_id)

    if request.method == 'POST':
        form = ResearchForm(request.POST or None,
                            files=request.FILES, instance=research)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل البحث بنجاح'))
            return redirect('research')

    else:
        form = ResearchForm(instance=research)

    context = {
        'research': research,
        'form': form,
    }
    return render(request, 'orgs/research/edit_research.html', context)


@login_required(login_url='signe_in')
def delete_research(request, research_id):
    research = get_object_or_404(OrgResearch, id=research_id)
    if request.method == 'POST' and request.user.is_superuser:
        research.delete()

        messages.success(request, _(
            'لقد تم حذف البحث بنجاح'))
        return redirect('research')
    context = {
        'research': research,
    }
    return render(request, 'orgs/research/delete_research.html', context)


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
# Recourses of civilty this is the befor last tab
def resources(request):
    return render(request, 'orgs/resources/org_recources.html')

####################################################################
# Org_jobs show all jobs with order by pub_at


def orgs_jobs(request):
    jobs = OrgJob.objects.filter(publish=True).order_by('-created_at')
    print(jobs)

    myFilter = OrgsJobsFilter(request.GET, queryset=jobs)
    jobs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(jobs, 12)
    page = request.GET.get('page')
    try:
        jobs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        jobs = paginator.page(paginator.num_pages)

    context = {
        'jobs': jobs,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/resources/org_jobs.html', context)
# add job to recourse


@login_required(login_url='signe_in')
def orgs_add_job(request):

    other = OtherOrgs.objects.all().count()

    if request.method == 'POST':
        form = JobsForm(request.POST or None, files=request.FILES)
        form_other = OtherOrgsForm(request.POST or None, files=request.FILES)
        if form.is_valid() and form_other.is_valid():
            user = form.save(commit=False)
            user.user = request.user

            org_name = form.cleaned_data.get('org_name')
            other_org_name = form.cleaned_data.get('other_org_name')
            other_name = form_other.cleaned_data.get('name')

            if org_name or other_org_name or other_name:
                user.org_name = org_name
            # else:
            #     user.org_name = request.user
                user.save()

                if other_name:
                    creater = form_other.save(commit=False)
                    creater.created_by = request.user
                    creater.job = form.instance.id
                    creater.save()

                messages.success(request, _(
                    'لقد تمت إضافة فرصة العمل بنجاح و ستتم دراستها قريباً'))

                return redirect('orgs_jobs')

            else:
                messages.error(request, _(
                    'يجب إدخال اسم منظمة لتتم معالجة و نشر فرصة العمل'))
    else:
        form = JobsForm()
        form_other = OtherOrgsForm()

    context = {
        'form': form,
        'other': other,
        'form_other': form_other,
    }
    return render(request, 'orgs/resources/org_add_job.html', context)
# jobs list to confirme


@login_required(login_url='signe_in')
def org_jobs_not_pub(request):
    jobs = OrgJob.objects.filter(publish=False).order_by('-created_at')
    others = OtherOrgs.objects.all()

    # PAGINATEUR
    paginator = Paginator(jobs, 12)
    page = request.GET.get('page')
    try:
        jobs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        news = paginator.page(paginator.num_pages)

    context = {
        'jobs': jobs,
        'others': others,
    }

    return render(request, 'orgs/resources/jobs_not_pub.html', context)


# job details
def jobs_detail(request, job_id):
    job = get_object_or_404(OrgJob, id=job_id)
    other = OtherOrgs.objects.filter(job=job_id).first()

    job_type = job.get_job_type_display()
    experience = job.get_experience_display()
    position_work = job.get_position_work_display()
    job_domain = job.get_job_domain_display()

    if request.method == 'POST':
        form = NewsConfirmForm(request.POST or None, instance=job)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تغيير حالة فرصة العمل بنجاح'))
            return redirect('orgs_jobs')
    else:
        form = JobsConfirmForm(instance=job)

    context = {
        'job': job,
        'form': form,
        'other': other,
        'job_type': job_type,
        'experience': experience,
        'position_work': position_work,
        'job_domain': job_domain,
    }
    return render(request, 'orgs/resources/org_job_details.html', context)
# job edit to modify job details


@login_required(login_url='signe_in')
def jobs_edit(request, job_id):
    job = get_object_or_404(OrgJob, id=job_id)
    other = OtherOrgs.objects.filter(job=job_id).first()
    # other = get_object_or_404(OtherOrgs, job=job_id)

    if request.method == 'POST':
        form = JobsForm(request.POST or None,
                        files=request.FILES, instance=job)
        form_other = OtherOrgsForm(
            request.POST or None, files=request.FILES, instance=other)
        if form.is_valid() and form_other.is_valid():
            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل فرصة العمل بنجاح'))
            return redirect('orgs_jobs')
    else:
        form = JobsForm(instance=job)
        form_other = OtherOrgsForm(instance=other)

    context = {
        'job': job,
        'form': form,
        'form_other': form_other,
    }
    return render(request, 'orgs/resources/org_edit_job.html', context)
# delete job


@login_required(login_url='signe_in')
def jobs_delete(request, job_id):
    job = get_object_or_404(OrgJob, id=job_id)

    if request.method == 'POST' and request.user.is_superuser:
        job.delete()

        messages.success(request, _(
            'لقد تم حذف فرصة العمل بنجاح'))
        return redirect('orgs_jobs')

    context = {
        'job': job,
    }
    return render(request, 'orgs/resources/org_job_delete.html', context)
#############################################################################
# FUNDING GENERAL


def funding(request):
    context = {

    }
    return render(request, 'orgs/funding_opport/funding.html', context)

# FINANCE PERSO PUB


def finance_perso(request):
    fundings = PersFundingOpp.objects.filter(
        publish=True).order_by('-created_at')

    myFilter = PersoFundFilter(request.GET, queryset=fundings)
    fundings = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(fundings, 12)
    page = request.GET.get('page')
    try:
        fundings = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        fundings = paginator.page(paginator.num_pages)

    context = {
        'fundings': fundings,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/funding_opport/pers/pub.html', context)


@login_required(login_url='signe_in')
def add_finance_perso(request):
    if request.method == 'POST':
        form = PersoFunForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            org_name = form.cleaned_data.get('org_name')
            name_funding = form.cleaned_data.get('name_funding')

            if org_name or name_funding:
                user = form.save(commit=False)
                user.user = request.user
                user.save()

                messages.success(request, _(
                    'لقد تم تسجيل طلب فرصة التمويل بنجاح و ستتم دراسته قريباً'))
                return redirect('finance_perso')
            else:
                messages.error(request, _(
                    'رجاءً أدخل اسم المنظمة أو الجهة المانحة لتتم دراسة فرصة التمويل'))
    else:
        form = PersoFunForm()

    context = {
        'form': form,
    }
    return render(request, 'orgs/funding_opport/pers/add.html', context)


# FINANCE PERSO DETAILS


def finance_perso_detail(request, pk):
    perso = get_object_or_404(PersFundingOpp, id=pk)
    persos = PersFundingOpp.objects.filter(
        publish=True).order_by('-created_at')

    if request.method == 'POST':
        form = PersoFundConfirmForm(request.POST or None, instance=perso)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تغيير حالة فرصة التمويل بنجاح'))
            return redirect('finance_perso')
    else:
        form = PersoFundConfirmForm(instance=perso)

    context = {
        'perso': perso,
        'persos': persos,
        'form': form,
    }
    return render(request, 'orgs/funding_opport/pers/detail.html', context)


@login_required(login_url='signe_in')
def finance_perso_edit(request, pk):
    perso = get_object_or_404(PersFundingOpp, id=pk)

    if request.method == 'POST':
        form = PersoFunForm(request.POST or None,
                            files=request.FILES, instance=perso)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل فرصة التمويل بنجاح'))
            return redirect('finance_perso')
    else:
        form = PersoFunForm(instance=perso)

    context = {
        'perso': perso,
        'form': form,
    }

    return render(request, 'orgs/funding_opport/pers/edit.html', context)


@login_required(login_url='signe_in')
def finance_perso_delete(request, pk):
    funding = get_object_or_404(PersFundingOpp, id=pk)

    if request.method == 'POST' and request.user.is_superuser:
        funding.delete()

        messages.success(request, _(
            'لقد تم حذف فرصة التمويل بنجاح'))
        return redirect('orgs_jobs')

    context = {
        'funding': funding,
    }
    return render(request, 'orgs/funding_opport/pers/delete.html', context)


@login_required(login_url='signe_in')
def finance_perso_not_pub(request):
    fundings = PersFundingOpp.objects.filter(
        publish=False).order_by('-created_at')
    myFilter = PersoFundFilter(request.GET, queryset=fundings)
    fundings = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(fundings, 12)
    page = request.GET.get('page')
    try:
        fundings = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        fundings = paginator.page(paginator.num_pages)

    context = {
        'fundings': fundings,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/funding_opport/pers/not_pub.html', context)


# funding org opp
def orgs_funding(request):
    fundings = OrgFundingOpp.objects.filter(
        publish=True).order_by('-created_at')

    myFilter = OrgsFundingFilter(request.GET, queryset=fundings)
    fundings = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(fundings, 12)
    page = request.GET.get('page')
    try:
        fundings = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        fundings = paginator.page(paginator.num_pages)

    context = {
        'fundings': fundings,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/funding_opport/orgs/org_funding.html', context)
# add funding


@login_required(login_url='signe_in')
def orgs_add_funding(request):

    if request.method == 'POST':
        form = FundingForm(request.POST or None, files=request.FILES)
        if form.is_valid():

            org_name = form.cleaned_data.get('org_name')
            name_funding = form.cleaned_data.get('name_funding')

            if org_name or name_funding:
                user = form.save(commit=False)
                user.user = request.user
                org_name = form.cleaned_data.get('org_name')
                if org_name:
                    user.org_name = org_name
                else:
                    user.org_name = request.user
                user.save()

                messages.success(request, _(
                    'لقد تمت إضافة فرصة التمويل بنجاح و ستتم دراسته قريباً'))

                return redirect('orgs_funding')
            else:
                messages.error(request, _(
                    'يحب إدخال اسم منظمة أو اسم الجهة المانحة لنتمكن من دراسة فرصة التمويل'))
    else:
        form = FundingForm()

    context = {
        'form': form,
    }
    return render(request, 'orgs/funding_opport/orgs/org_add_funding.html', context)
# funding list to confirme


@login_required(login_url='signe_in')
def org_funding_not_pub(request):
    fundings = OrgFundingOpp.objects.filter(
        publish=False).order_by('-created_at')

    # PAGINATEUR
    paginator = Paginator(fundings, 12)
    page = request.GET.get('page')
    try:
        fundings = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        fundings = paginator.page(paginator.num_pages)

    context = {
        'fundings': fundings,
    }
    return render(request, 'orgs/funding_opport/orgs/fundings_not_pub.html', context)
# funding details


def funding_detail(request, funding_id):
    funding = get_object_or_404(OrgFundingOpp, id=funding_id)
    fundings = OrgFundingOpp.objects.filter(
        publish=True).order_by('-created_at')

    if request.method == 'POST':
        form = FundingConfirmForm(request.POST or None, instance=funding)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تغيير حالة المنحة  بنجاح'))
            return redirect('orgs_funding')
    else:
        form = FundingConfirmForm(instance=funding)

    context = {
        'funding': funding,
        'form': form,
        'fundings': fundings,
    }
    return render(request, 'orgs/funding_opport/orgs/org_funding_details.html', context)
# job edit to modify job details


@login_required(login_url='signe_in')
def funding_edit(request, funding_id):
    funding = get_object_or_404(OrgFundingOpp, id=funding_id)

    if request.method == 'POST':
        form = FundingForm(request.POST or None,
                           files=request.FILES, instance=funding)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل فرصة التمويل بنجاح'))
            return redirect('orgs_funding')
    else:
        form = FundingForm(instance=funding)

    context = {
        'funding': funding,
        'form': form,
    }
    return render(request, 'orgs/funding_opport/orgs/org_edit_funding.html', context)
# delete funding


@login_required(login_url='signe_in')
def funding_delete(request, funding_id):
    funding = get_object_or_404(OrgFundingOpp, id=funding_id)

    if request.method == 'POST' and request.user.is_superuser:
        funding.delete()

        messages.success(request, _(
            'لقد تم حذف فرصة التمويل بنجاح'))
        return redirect('orgs_funding')

    context = {
        'funding': funding,
    }
    return render(request, 'orgs/funding_opport/orgs/org_funding_delete.html', context)


# Capacity buildinng for opportunities
def orgs_capacity(request):
    Capacitys = OrgCapacityOpp.objects.filter(
        publish=True).order_by('-created_at')

    myFilter = OrgsCapacityFilter(request.GET, queryset=Capacitys)
    Capacitys = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(Capacitys, 12)
    page = request.GET.get('page')

    try:
        Capacitys = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        Capacitys = paginator.page(paginator.num_pages)

    context = {
        'Capacitys': Capacitys,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/capacity/org_capacity.html', context)
# add funding


@login_required(login_url='signe_in')
def orgs_add_capacity(request):

    if request.method == 'POST':
        form = CapacityForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            org_name = form.cleaned_data.get('org_name')
            name_capacity = form.cleaned_data.get('name_capacity')
            if org_name or name_capacity:
                user = form.save(commit=False)
                user.user = request.user
                org_name = form.cleaned_data.get('org_name')
                if org_name:
                    user.org_name = org_name
                else:
                    user.org_name = request.user
                user.save()

                messages.success(request, _(
                    'لقد تمت إضافة فرصة بناء القدرات بنجاح و ستتم دراسته قريباً'))

                return redirect('orgs_capacity')
            else:
                messages.error(request, _(
                    'يجب إدخال اسم الجهة المانحة لنتمكن من دراسة الفرصة'))
    else:
        form = CapacityForm()

    context = {
        'form': form,
    }
    return render(request, 'orgs/capacity/org_add_capacity.html', context)
# funding list to confirme


@login_required(login_url='signe_in')
def org_capacity_not_pub(request):
    Capacitys = OrgCapacityOpp.objects.filter(
        publish=False).order_by('-created_at')

    # PAGINATEUR
    paginator = Paginator(Capacitys, 12)
    page = request.GET.get('page')
    try:
        Capacitys = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        Capacitys = paginator.page(paginator.num_pages)

    context = {
        'Capacitys': Capacitys,
    }
    return render(request, 'orgs/capacity/capacity_not_pub.html', context)
# capacity details


def capacity_detail(request, capacity_id):
    capacity = get_object_or_404(OrgCapacityOpp, id=capacity_id)

    if request.method == 'POST':
        form = CapacityConfirmForm(request.POST or None, instance=capacity)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تغيير حالة فرصة بناء القدرات  بنجاح'))
            return redirect('orgs_capacity')
    else:
        form = CapacityConfirmForm(instance=capacity)

    context = {
        'capacity': capacity,
        'form': form,
    }
    return render(request, 'orgs/capacity/org_capacity_details.html', context)
# capacity edit to modify capacity details


@login_required(login_url='signe_in')
def capacity_edit(request, capacity_id):
    capacity = get_object_or_404(OrgCapacityOpp, id=capacity_id)

    if request.method == 'POST':
        form = CapacityForm(request.POST or None,
                            files=request.FILES, instance=capacity)
        if form.is_valid():
            print('salut')
            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل فرصة بناء القدرات بنجاح'))

            return redirect('orgs_capacity')
        else: 
            messages.error(request, 'the form is not valide')
    else:
        form = CapacityForm(instance=capacity)

    context = {
        'capacity': capacity,
        'form': form,
    }
    return render(request, 'orgs/capacity/org_edit_capacity.html', context)
# delete funding


@login_required(login_url='signe_in')
def capacity_delete(request, capacity_id):
    capacity = get_object_or_404(OrgCapacityOpp, id=capacity_id)

    if request.method == 'POST' and request.user.is_superuser:
        capacity.delete()

        messages.success(request, _(
            'لقد تم حذف فرصة بناء القدرات بنجاح'))
        return redirect('orgs_capacity')

    context = {
        'capacity': capacity,
    }
    return render(request, 'orgs/capacity/org_capacity_delete.html', context)
# dev orgs guide devs


def orgs_devs(request):
    devs = DevOrgOpp.objects.filter(publish=True).order_by('-created_at')

    myFilter = OrgsDevFilter(request.GET, queryset=devs)
    devs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(devs, 12)
    page = request.GET.get('page')
    try:
        devs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        devs = paginator.page(paginator.num_pages)

    context = {
        'devs': devs,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/devs/org_devs.html', context)
# add devs


@login_required(login_url='signe_in')
def orgs_add_devs(request):

    if request.method == 'POST':
        form = DevForm(request.POST or None, files=request.FILES)
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
                'لقد تمت إضافة دليل تطوير بنجاح و ستتم دراسته قريباً'))

            return redirect('orgs_devs')
    else:
        form = DevForm()

    context = {
        'form': form,
    }
    return render(request, 'orgs/devs/org_add_dev.html', context)
# devs list to confirme 0


@login_required(login_url='signe_in')
def org_devs_not_pub(request):
    devs = DevOrgOpp.objects.filter(publish=False).order_by('-created_at')

    # PAGINATEUR
    paginator = Paginator(devs, 12)
    page = request.GET.get('page')
    try:
        devs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        devs = paginator.page(paginator.num_pages)

    context = {
        'devs': devs,
    }
    return render(request, 'orgs/devs/dev_not_pub.html', context)
# devs details


def devs_detail(request, devs_id):
    devs = get_object_or_404(DevOrgOpp, id=devs_id)

    if request.method == 'POST':
        form = DevConfirmForm(request.POST or None, instance=devs)
        if form.is_valid():
            at = form.save(commit=False)
            at.published_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تغيير حالة دليل تطوير بنجاح'))
            return redirect('orgs_devs')
    else:
        form = DevConfirmForm(instance=devs)

    context = {
        'devs': devs,
        'form': form,
    }
    return render(request, 'orgs/devs/org_dev_details.html', context)
# dev edit to modify dev details


@login_required(login_url='signe_in')
def dev_edit(request, devs_id):
    devs = get_object_or_404(DevOrgOpp, id=devs_id)

    if request.method == 'POST':
        form = DevForm(request.POST or None,
                       files=request.FILES, instance=devs)
        if form.is_valid():
            at = form.save(commit=False)
            at.updated_at = datetime.utcnow()
            at.save()

            messages.success(request, _(
                'لقد تم تعديل دليل التطوير بنجاح'))
            return redirect('orgs_devs')
    else:
        form = DevForm(instance=devs)

    context = {
        'devs': devs,
        'form': form,
    }
    return render(request, 'orgs/devs/org_edit_dev.html', context)


# delete dev bulding
@login_required(login_url='signe_in')
def dev_delete(request, devs_id):
    devs = DevOrgOpp.objects.filter(publish=True).order_by('-created_at')

    myFilter = OrgsDevFilter(request.GET, queryset=devs)
    devs = myFilter.qs

    # PAGINATEUR
    paginator = Paginator(devs, 12)
    page = request.GET.get('page')
    try:
        devs = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        devs = paginator.page(paginator.num_pages)

    context = {
        'devs': devs,
        'myFilter': myFilter,
    }
    return render(request, 'orgs/devs/org_devs.html', context)


# @login_required(login_url='signe_in')
# def dev_delete(request, devs_id):
#     devs = get_object_or_404(DevOrgOpp, id=devs_id)

#     if request.method == 'POST' and request.user.is_superuser:
# 	devs.delete()

# 	messages.success(request, _(
#             'لقد تم حذف دليل التطوير بنجاح'))
# 	return redirect('orgs_devs')


# our news is filter of all the news that publiched by our site


def orgs_our_news(request):
    news = OrgNews.objects.filter(Q(publish=True) & Q(
        org_name__name='khalil')).order_by('-created_at')

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
    return render(request, 'orgs/our_news/our_news.html', context)
