from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages
import os
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.core.mail import EmailMessage
from django.utils.timezone import datetime
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from .filters import *
from django.db.models import Q
from datetime import date, timedelta
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.embed import components
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

# if OrgProfile.objects.filter(id=user.id).exists():

# add profile


@login_required(login_url='signe_in')
def org_profile(request):

    users = OrgProfile.objects.all()
    orgs = []
    for user in users:
        orgs += user.user.id,
    # print('==========', orgs)

    if request.method == 'POST':
        form = OrgProfileForm(request.POST or None, files=request.FILES)

        if request.POST.get('user') != None:
            userprof = request.POST.get('user')
        else:
            userprof = request.user.id
        # print('==========', userprof)

        if int(userprof) not in orgs:
            print('is not in')
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
            if int(userprof) in orgs and not request.user.is_staff:
                # print(orgs)
                # print('is in')
                messages.error(request, _('هذا المستخدم ليه طلب مسبقاً'))
                return redirect('org_profile')

    else:
        form = OrgProfileForm()

    context = {
        'form': form
    }
    return render(request, 'profiles/org_profile_form.html', context)


# update

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


# etude
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

# L'AFFICHAGE DES ORGS NOT PUBLISHED


def guide_not_pub(request):
    orgs = OrgProfile.objects.filter(publish=False).order_by('-created_at')

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
    return render(request, 'orgs/guid/orgs_guid_conf_pub.html', context)


# published

@login_required(login_url='signe_in')
def orgs_orders_published(request):
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
    return render(request, 'profiles/orgs_orders_published.html', context)


# ORG DETAIL تفاصيل المنظمة مع الموافقة و الرفض
def particip_detail(request, par_id):
    org = get_object_or_404(OrgProfile, id=par_id)

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
    }
    return render(request, 'profiles/particip_detail.html', context)


# PROFILE
@login_required(login_url='signe_in')
def profile(request):

    if request.user.is_superuser:
        return redirect('profile_supper')

    if request.user.is_staff:
        return redirect('profile_staff')

    # profs = OrgProfile.objects.filter(user=request.user)
    profs = OrgProfile.objects.all().filter(user=request.user)

    user_prof = OrgProfile.objects.filter(user=request.user)
    #     user_prof = ''
    # else:
    #     user_prof = OrgProfile.objects.get(user=request.user)

    context = {
        'profs': profs,
        'user_prof': user_prof,
    }
    return render(request, 'profiles/profile.html', context)


# staff profile
@login_required(login_url='signe_in')
def profile_staff(request):
    if request.user.is_staff:
        profs = OrgProfile.objects.all()

        context = {
            'profs': profs,
        }
        return render(request, 'profiles/staff_profile.html', context)
    else:
        return redirect('profile')


# delete profile


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


# admin dashboard to return the count of all objects in our models each one in dependant
@login_required(login_url='signe_in')
def admin_dashboard(request):

    if request.user.is_superuser:
        # filter without 'org_name'
        orgs = OrgProfile.objects.all()
        myFilter_orgs = OrgsFilter(request.GET, queryset=orgs)
        orgs_count = myFilter_orgs.qs.count()
        researchs = OrgResearch.objects.filter(
            publish=True).order_by('-created_at')
        myFilter = OrgsFilter(request.GET, queryset=researchs)
        researchs_count = myFilter.qs.count()
        # filter with 'org_name'
        news = OrgNews.objects.filter(Q(publish=True) & ~Q(
            org_name__name='khalil')).order_by('-created_at')
        myFilter = OrgsNewsFilter(request.GET, queryset=news)
        news_count = myFilter.qs.count()
        rapports = OrgRapport.objects.filter(
            publish=True).order_by('-created_at')
        myFilter = OrgsNewsFilter(request.GET, queryset=rapports)
        rapports_count = myFilter.qs.count()
        datas = OrgData.objects.filter(publish=True).order_by('-created_at')
        myFilter = OrgsNewsFilter(request.GET, queryset=datas)
        datas_count = myFilter.qs.count()
        medias = OrgMedia.objects.filter(publish=True).order_by('-created_at')
        myFilter = OrgsNewsFilter(request.GET, queryset=medias)
        medias_count = myFilter.qs.count()
        jobs = OrgJob.objects.filter(publish=True).order_by('-created_at')
        myFilter = OrgsNewsFilter(request.GET, queryset=jobs)
        jobs_count = myFilter.qs.count()
        fundings = OrgFundingOpp.objects.filter(
            publish=True).order_by('-created_at')
        myFilter = OrgsNewsFilter(request.GET, queryset=fundings)
        fundings_count = myFilter.qs.count()
        Capacitys = OrgCapacityOpp.objects.filter(
            publish=True).order_by('-created_at')
        myFilter = OrgsNewsFilter(request.GET, queryset=Capacitys)
        Capacitys_count = myFilter.qs.count()
        devs = DevOrgOpp.objects.filter(publish=True).order_by('-created_at')
        myFilter = OrgsNewsFilter(request.GET, queryset=devs)
        devs_count = myFilter.qs.count()
        our_news = OrgNews.objects.filter(Q(publish=True) & Q(
            org_name__name='khalil')).order_by('-created_at')
        myFilter = OrgsNewsFilter(request.GET, queryset=our_news)
        our_news_count = myFilter.qs.count()
        # data visualation
        sdate = str(datetime.now().date()-timedelta(days=6))
        edate = str(datetime.now().date())
        if request.GET:
            sdate = request.GET.get('start_date_pub')
            edate = request.GET.get('end_date_pub')
            if sdate == '':
                sdate = str(datetime.now().date()-timedelta(days=6))
            if edate == '':
                edate = str(datetime.now().date())
        days = []
        delta = datetime.strptime(
            edate, '%Y-%m-%d').date() - datetime.strptime(sdate, '%Y-%m-%d').date()
        for i in range(delta.days + 1):
            day = datetime.strptime(
                sdate, '%Y-%m-%d').date() + timedelta(days=i)
            days.append(day)
        # news per day
        days_to_present = []
        counts = []
        if request.GET:
            org_name = request.GET.get('org_name', None)
            if org_name == '':
                for i in range(len(days)):
                    days_to_present.append(str(days[i]))
                    counts.append(OrgNews.objects.filter(
                        Q(publish=True) & Q(published_at__date=days[i])).count())

            else:
                for i in range(len(days)):
                    days_to_present.append(str(days[i]))
                    counts.append(OrgNews.objects.filter(Q(publish=True) & Q(
                        published_at__date=days[i]) & Q(org_name__id=org_name)).count())
        else:
            for i in range(len(days)):
                days_to_present.append(str(days[i]))
                counts.append(OrgNews.objects.filter(
                    Q(publish=True) & Q(published_at__date=days[i])).count())

        source = ColumnDataSource(
            data=dict(days_to_present=days_to_present, counts=counts))
        factor_cmap('', palette=Spectral6, factors=days_to_present)
        TOOLTIPS = [
            ('date', "@days_to_present"),
            ('count', "@counts"),

        ]
        p = figure(x_range=days_to_present, plot_height=250, title="عدد الأخبار المنشورة باليوم",
                   tools="pan,wheel_zoom,box_zoom,save,zoom_in,hover,zoom_out,reset", tooltips=TOOLTIPS)
        p.vbar(x='days_to_present', top='counts', width=0.9, source=source, legend_field="days_to_present",
               line_color='white', fill_color=factor_cmap('days_to_present', palette=Spectral6, factors=days_to_present))
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.y_range.start = 0
        p.background_fill_color = "rgb(255, 255, 255)"
        p.border_fill_color = "rgb(255, 255, 255)"
        # p.background_fill_color = "rgba(23, 103, 140, 0.1)"
        # p.border_fill_color = "rgba(23, 103, 140, 0.1)"
        p.title.align = 'center'
        p.legend.visible = False
        script, div = components(p)
        # orgs by days
        counts_org = []
        for i in range(len(days)):
            counts_org.append(OrgProfile.objects.filter(
                Q(publish=True) & Q(published_at__date=days[i])).count())

        source = ColumnDataSource(
            data=dict(days_to_present=days_to_present, counts_org=counts_org))
        factor_cmap('days_to_present', palette=Spectral6,
                    factors=days_to_present)
        TOOLTIPS = [
            ('name', "@days_to_present"),
            ('count', "@counts_org"),

        ]
        p_org = figure(x_range=days_to_present, plot_height=250, title="عدد المنظمات المنشورة باليوم",
                       tools="pan,wheel_zoom,box_zoom,save,zoom_in,hover,zoom_out,reset", tooltips=TOOLTIPS)
        p_org.vbar(x='days_to_present', top='counts_org', width=0.9, source=source, legend_field="days_to_present",
                   line_color='white', fill_color=factor_cmap('days_to_present', palette=Spectral6, factors=days_to_present))
        p_org.xgrid.grid_line_color = None
        p_org.ygrid.grid_line_color = None
        p_org.y_range.start = 0
        p_org.background_fill_color = "rgb(255, 255, 255)"
        p_org.border_fill_color = "rgb(255, 255, 255)"
        p_org.title.align = 'center'
        p_org.legend.visible = False
        script_org, div_org = components(p_org)
        # reports by days
        counts_report = []
        if request.GET:
            org_name = request.GET.get('org_name', None)
            if org_name == '':
                for i in range(len(days)):
                    counts_report.append(OrgRapport.objects.filter(
                        Q(publish=True) & Q(published_at__date=days[i])).count())

            else:
                for i in range(len(days)):
                    counts_report.append(OrgRapport.objects.filter(Q(publish=True) & Q(
                        published_at__date=days[i]) & Q(org_name__id=org_name)).count())
        else:
            for i in range(len(days)):
                counts_report.append(OrgRapport.objects.filter(
                    Q(publish=True) & Q(published_at__date=days[i])).count())

        source = ColumnDataSource(
            data=dict(days_to_present=days_to_present, counts_report=counts_report))
        factor_cmap('', palette=Spectral6, factors=days_to_present)
        TOOLTIPS = [
            ('name', "@days_to_present"),
            ('count', "@counts_report"),

        ]
        p_report = figure(x_range=days_to_present, plot_height=250, title="عدد التقارير المنشورة باليوم",
                          tools="pan,wheel_zoom,box_zoom,save,zoom_in,hover,zoom_out,reset", tooltips=TOOLTIPS)
        p_report.vbar(x='days_to_present', top='counts_report', width=0.9, source=source, legend_field="days_to_present",
                      line_color='white', fill_color=factor_cmap('days_to_present', palette=Spectral6, factors=days_to_present))
        p_report.xgrid.grid_line_color = None
        p_report.ygrid.grid_line_color = None
        p_report.y_range.start = 0
        p_report.background_fill_color = "rgb(255, 255, 255)"
        p_report.border_fill_color = "rgb(255, 255, 255)"
        p_report.title.align = 'center'
        p_report.legend.visible = False
        script_report, div_report = components(p_report)
        # jobs per days
        counts_jobs = []
        if request.GET:
            org_name = request.GET.get('org_name', None)
            if org_name == '':
                for i in range(len(days)):
                    counts_jobs.append(OrgJob.objects.filter(
                        Q(publish=True) & Q(published_at__date=days[i])).count())

            else:
                for i in range(len(days)):
                    counts_jobs.append(OrgJob.objects.filter(Q(publish=True) & Q(
                        published_at__date=days[i]) & Q(org_name__id=org_name)).count())
        else:
            for i in range(len(days)):
                counts_jobs.append(OrgJob.objects.filter(
                    Q(publish=True) & Q(published_at__date=days[i])).count())

        source = ColumnDataSource(
            data=dict(days_to_present=days_to_present, counts_jobs=counts_jobs))
        factor_cmap('', palette=Spectral6, factors=days_to_present)
        TOOLTIPS = [
            ('name', "@days_to_present"),
            ('count', "@counts_jobs"),

        ]
        p_jobs = figure(x_range=days_to_present, plot_height=250, title="عدد التقارير المنشورة باليوم",
                        tools="pan,wheel_zoom,box_zoom,save,zoom_in,hover,zoom_out,reset", tooltips=TOOLTIPS)
        p_jobs.vbar(x='days_to_present', top='counts_jobs', width=0.9, source=source, legend_field="days_to_present",
                    line_color='white', fill_color=factor_cmap('days_to_present', palette=Spectral6, factors=days_to_present))
        p_jobs.xgrid.grid_line_color = None
        p_jobs.ygrid.grid_line_color = None
        p_jobs.y_range.start = 0
        p_jobs.background_fill_color = "rgb(255, 255, 255)"
        p_jobs.border_fill_color = "rgb(255, 255, 255)"
        p_jobs.title.align = 'center'
        p_jobs.legend.visible = False
        script_jobs, div_jobs = components(p_jobs)

        # v_count = OrgNews.objects.filter(Q(publish=True)& Q(published_at__date='2020-11-05')).count()
        # for pro in profs:
        #     org_type = pro.get_org_type_display()
        #     position_work = pro.get_position_work_display()
        #     # city_work = pro.get_city_work_display()
        #     work_domain = pro.get_work_domain_display()
        #     target_cat = pro.get_target_cat_display()
        #     org_registered_country = pro.get_org_registered_country_display()
        #     w_polic_regulations = pro.get_w_polic_regulations_display()

        context = {

            # 'org_type': org_type,
            # 'position_work': position_work,
            # # 'city_work': city_work,
            # 'work_domain': work_domain,
            # 'target_cat': target_cat,
            # 'org_registered_country': org_registered_country,
            # 'w_polic_regulations': w_polic_regulations,
            'news_count': news_count,
            'myFilter': myFilter,
            'orgs_count': orgs_count,
            'myFilter_orgs': myFilter_orgs,
            'rapports_count': rapports_count,
            'datas_count': datas_count,
            'medias_count': medias_count,
            'researchs_count': researchs_count,
            'jobs_count': jobs_count,
            'fundings_count': fundings_count,
            'Capacitys_count': Capacitys_count,
            'devs_count': devs_count,
            'our_news_count': our_news_count,
            # 'sdate':sdate,
            # 'edate':edate,
            'days': days,
            'delta': delta,
            'script': script,
            'div': div,
            'script_org': script_org,
            'div_org': div_org,
            'script_report': script_report,
            'div_report': div_report,
            'script_jobs': script_jobs,
            'div_jobs': div_jobs,
            #  'org_name':org_name
        }

    else:
        return HttpResponse('You dont have the permitions to entro this page :) ')

    return render(request, 'profiles/layout_profile.html', context)
# this is to export into excel for the next step
# def export_data(request):
#                   objs = OrgJob.objects.all()
#                   return ExcelResponse(objs)
