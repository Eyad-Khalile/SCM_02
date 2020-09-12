from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'orgs/home.html')

def guide(request):
    return render(request, 'orgs/orgs_guide.html')

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
    return render(request, 'orgs/orgs_guide_filter.html', context)


def news(request):
    return render(request, 'orgs/orgs_news.html')

def news_detail(request, news_id):
    id = news_id
    context = {
        'id': id,
    }
    return render(request, 'orgs/orgs_news_detail.html', context)

def orgs_news(request):
    return render(request, 'orgs/orgs_news_news.html')

def signe_in(request):
    return render(request, 'register/signe-in.html')

def signe_up(request):
    return render(request, 'register/signe-up.html')

def site_politic(request):
    return render(request, 'orgs/politic.html')

def particip_detail(request, par_id):
    context = {
        'par_id': par_id,
    }
    return  render(request, 'orgs/particip_detail.html', context)

def orgs_rapport(request):
    return render(request, 'orgs/orgs_rapport.html')

def orgs_rapport_detail(request, rapport_id):
    id = rapport_id
    context = {
        'id': id,
    }
    return render(request, 'orgs/orgs_rapport_detail.html', context)

def data(request):
    return render(request, 'orgs/orgs_data.html')

def data_detail(request, data_id):
    id = data_id
    context = {
        'id': id,
    }
    return render(request, 'orgs/orgs_data_detail.html', context)

def media(request):
    return render(request, 'orgs/orgs_media.html')

def media_detail(request, media_id):
    id = media_id
    context = {
        'id': id,
    }
    return render(request, 'orgs/orgs_media_detail.html', context)

def research(request):
    return render(request, 'orgs/orgs_research.html')

def research_detail(request, res_id):
    id = res_id
    context = {
        'id': id,
    }
    return render(request, 'orgs/orgs_research_detail.html', context)

# RECOURCE
def resource(request):
    return render(request, 'orgs/resource.html')

def resource_work(request):
    return render(request, 'orgs/resource_work.html')

def resource_work_detail(request, work_id):
    id = work_id
    context = {
        'id': id,
    }
    return render(request, 'orgs/resource_work_detail.html', context)

def resource_finance(request):
    return render(request, 'orgs/resource_finance.html')

def resource_finance_perso(request):
    return render(request, 'orgs/resource_finance_perso.html')

def resource_finance_perso_detail(request, id):
    id = id 
    context = {
        'id': id,
    }
    return render(request, 'orgs/resource_finance_perso_detail.html', context)

def resource_finance_orgs(request):
    return render(request, 'orgs/resource_finance_orgs.html')

def resource_finance_orgs_detail(request, id):
    id = id 
    context = {
        'id': id,
    }
    return render(request, 'orgs/resource_finance_orgs_detail.html', context)

def resource_stectur(request):
    return render(request, 'orgs/resource_strectur.html')

def resource_stectur_detail(request, id):
    id = id
    context = {
        'id': id,
    }
    return render(request, 'orgs/resource_strectur_detail.html', context)

def resource_upgrade(request):
    return render(request, 'orgs/resource_upgrade.html')

def resource_upgrade_detail(request, id):
    id = id
    context = {
        'id': id,
    }
    return render(request, 'orgs/resource_upgrade_detail.html', context)


# CENTRE NEWS
def centre_news(request):
    return render(request, 'orgs/centre_news.html')

def centre_news_detail(request, id):
    id = id 

    context = {
        'id': id,
    }
    return render(request, 'orgs/centre_news_detail.html', context)


# CONTACT-US
# def contact(request):
#     return render(request, 'contact/contact.html')