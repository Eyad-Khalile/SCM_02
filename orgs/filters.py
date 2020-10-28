import django_filters
from django_filters import DateFilter, CharFilter
from .models import OrgProfile, OrgNews, OrgRapport, OrgData, OrgResearch
from django.utils.translation import gettext_lazy as _


class OrgsFilter(django_filters.FilterSet):
    # langue
    # language = CharFilter(field_name="language",label='Langue')
    # auther = CharFilter(field_name="auther", lookup_expr='gte',label='Auteur')
    # category = CharFilter(field_name="category", label='Catégorie')
    # sub_category = CharFilter(label='Sous-Catégorie')

    start_date = DateFilter(field_name="date_of_establishment",
                            lookup_expr='gte', label=_('تاريخ التأسيس / من :'))
    end_date = DateFilter(field_name="date_of_establishment",
                          lookup_expr='lte', label=_('إلى :'))
    name = CharFilter(field_name="name",
                      lookup_expr='icontains', label=_('اسم المنظمة'))
    # description = CharFilter(field_name="description",
    #                          lookup_expr='icontains', label='Description')

    class Meta:
        model = OrgProfile
        fields = [
            'name',
            'position_work',
            'work_domain',
            'start_date',
            'end_date',
            'target_cat',
        ]

        # exclude = ['date_published', 'date_updated', 'likes', 'is_published']


class OrgsNewsFilter(django_filters.FilterSet):

    title = CharFilter(field_name="title",
                       lookup_expr='icontains', label=_('كلمات من عنوان الخبر'))
    content = CharFilter(field_name="content",
                         lookup_expr='icontains', label=_('كلمات من تفاصيل الخبر'))

    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر الخبر / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgNews
        fields = [
            'org_name',
            'title',
            'content',
            'start_date_pub',
            'end_date_pub',
        ]


class OrgsRapportFilter(django_filters.FilterSet):

    title = CharFilter(field_name="title",
                       lookup_expr='icontains', label=_('كلمات من عنوان التقرير'))

    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر التقرير / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgRapport
        fields = [
            'org_name',
            'title',
            'domain',
            'start_date_pub',
            'end_date_pub',
        ]


class OrgsDataFilter(django_filters.FilterSet):

    title = CharFilter(field_name="title",
                       lookup_expr='icontains', label=_('كلمات من عنوان البيان'))

    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر البيان / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgData
        fields = [
            'org_name',
            'title',
            'start_date_pub',
            'end_date_pub',
        ]


class OrgsMediaFilter(django_filters.FilterSet):

    title = CharFilter(field_name="title",
                       lookup_expr='icontains', label=_('كلمات من عنوان المحتوى'))

    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر المحتوى / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgData
        fields = [
            'org_name',
            'title',
            'start_date_pub',
            'end_date_pub',
        ]


class OrgsResearchFilter(django_filters.FilterSet):
    name_entity = CharFilter(field_name="name_entity",
                             lookup_expr='icontains', label=_('كلمات من اسم الجهة'))
    title = CharFilter(field_name="title",
                       lookup_expr='icontains', label=_('كلمات من عنوان البحث'))

    start_date_pub = DateFilter(field_name="created_at",
                                lookup_expr='gte', label=_('تاريخ نشر البحث / من :'))
    end_date_pub = DateFilter(field_name="created_at",
                              lookup_expr='lte', label=_('إلى :'))

    class Meta:
        model = OrgResearch
        fields = [
            'name_entity',
            'title',
            'domaine',
            'start_date_pub',
            'end_date_pub',
        ]
