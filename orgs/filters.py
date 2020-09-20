import django_filters
from django_filters import DateFilter, CharFilter
from .models import OrgProfile
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
