from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class OrgProfile(models.Model):

    type_CHOICES = (
        ('establishment', _('مؤسسة')),
        ('org', _('جمعية أو منظمة')),
        ('team', _('مبادرة / فريق')),
        ('union', _('اتحاد / تحالف / تجمع')),
        ('group', _('لجنة / تنسيقية / مجموعة'))
    )

    city_CHOICES = (
        ('aleppo', _('حلب')),
        ('damascus', _('دمشق')),
        ('suburb of damascus', _('ريف دمشق')),
        ('daraa', _('درعا')),
        ('deir ez-Zor', _('دير الزور')),
        ('hama', _('حماه')),
        ('al-Hasakah', _('الحسكة')),
        ('homs', _('حمص')),
        ('idlib', _('إدلب')),
        ('latakia', _('اللاذقية')),
        ('quneitra', _('القنيطرة')),
        ('raqqa', _('الرقة')),
        ('as-Suwayda', _('السويداء')),
        ('tartus', _('طرطوس')),
    )

    domain_CHOICES = (
        ('Media', _('إعلام')),
        ('Education', _('تعليم')),
        ('Protection', _('حماية')),
        ('Livelihoods and food security', _('سبل العيش والأمن الغذائي')),
        ('Project of clean ,water, sanitation ', _(
            'مشاريع النظافة والمياه والصرف الصحي')),
        ('Development', _('تنمية')),
        ('Law, suport, policy', _('قانون و مناصرة و سیاسة')),
        ('Donors and support volunteering', _('مانحین و دعم العمل التطوعي')),
        ('Religious org', _('منظمات دینیة')),
        ('Prof association and assembles', _('تجمعات و اتحادات مھنیة')),
        ('Health', _('صحة')),
        ('Studies and research', _('دراسات وأبحاث')),
        ('Other', _('أخرى')),
    )

    target_CHOICES = (
        ('No category selected', _('لا يوجد فئة محددة')),
        ('womans', _('نساء')),
        ('Mans', _('رجال')),
        ('Youth 18-24', _('شباب 18-24')),
        ('Child 0-18', _('أطفال 0-18')),
        ('Religious groups', _('مجموعات دینیة')),
        ('Ethnic groups', _('مجموعة عرقیة')),
        ('Persons lacking breadwinner ', _('فاقدي المعیل')),
        ('Handicapped', _('ذوي الاحتیاجات الخاصة')),
        ('Refugees', _('لاجئین')),
        ('Displaced', _('نازحین')),
        ('Returned', _('عائدین')),
        ('Other civil society organizations', _('منظمات مجتمع مدني اخرى')),
        ('Other', _('أخرى')),
    )

    bool_CHOICES = (
        ('0', _('لا')),
        ('1', _('نعم')),
    )

    polic_CHOICES = (
        ('No', _('لا يوجد')),
        ('Code of conduct', _('مدونة السلوك')),
        ('Child protection', _('حماية الطفل')),
        ('Anti-corruption', _('مكافحة الفساد')),
        ('Human resources policy', _('سياسة الموارد البشرية')),
        ('Procurement policy', _('سياسة المشتريات')),
        ('Volunteering policy', _('سياسة التطوع')),
        ('Anti-harassment Policy', _('سياسة منع التحرش')),
        ('Financial policy', _('السياسة المالية')),
        ('Equipment use Policy', _('سياسة استخدام المعدات')),
        ('privacy policy', _('سياسة الخصوصية')),
        ('Other', _('أخرى')),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, null=False,
                            verbose_name=_("اسم المنظمة"))
    name_en_ku = models.CharField(max_length=255, null=True, blank=True,
                                  verbose_name=_("اسم المنظمة باللغة الانكليزية أو الكردية"))
    short_cut = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("الاسم المختصر"))
    org_type = models.CharField(
        max_length=150, null=False, choices=type_CHOICES, verbose_name=_("نوع المنظمة"))
    position_work = CountryField(
        max_length=255, null=False, verbose_name=_("مكان العمل"))
    city_work = models.CharField(
        max_length=150, choices=city_CHOICES, null=True, blank=True, verbose_name=_("المحافظة"))
    logo = models.ImageField(upload_to="org_logos",
                             null=False, default='org_logos/default_logo.jpg', verbose_name=_("شعار المنظمة"))
    message = models.TextField(
        max_length=2000, null=False, verbose_name=_("الرؤية و الرسالة"))

    name_managing_director = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("اسم رئيس مجلس اﻹدارة"))
    name_ceo = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('اسم المدير التنفيذي'))

    # CONTACT INFO
    site_web = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('الموقع الالكتروني'))
    facebook = models.URLField(
        max_length=255, null=True, blank=True, verbose_name=_('صفحة فيسبوك'))
    twitter = models.URLField(
        max_length=255, null=True, blank=True, verbose_name=_('صفحة تويتر'))
    email = models.EmailField(max_length=255, null=True,
                              blank=True, verbose_name=_('البريد الاكتروني'))
    phone = models.CharField(max_length=100, null=True,
                             blank=True, verbose_name=_('رقم الهاتف'))
    name_person_contact = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('اسم الشخص المسؤول عن التواصل'))
    email_person_contact = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('البريد الاكتروني للشخص المسؤول عن التواصل'))
    org_adress = models.CharField(
        max_length=255, null=False, verbose_name=_('عنوان المقر الرئيسي'))

    # ORG INFO
    work_domain = models.CharField(
        max_length=255, choices=domain_CHOICES, null=False, verbose_name=_('مجال العمل'))
    target_cat = models.CharField(
        max_length=255, null=False, choices=target_CHOICES, verbose_name=_('الفئات المستهدفة'))
    date_of_establishment = models.CharField(
        max_length=150, null=True, blank=True, verbose_name=_('تاريخ سنة التأسيس'))
    is_org_registered = models.CharField(
        max_length=100, null=False, choices=bool_CHOICES, verbose_name=_('هل المنظمة مسجلة ؟'))
    org_registered_country = CountryField(
        max_length=255, null=True, blank=True, verbose_name=_("بلد التسجيل"))

    org_members_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True, verbose_name=_('عدد اﻷعضاء'))
    org_members_womans_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True, verbose_name=_('عدد النساء من اﻷعضاء'))
    w_polic_regulations = models.CharField(
        max_length=200, null=False, choices=polic_CHOICES, verbose_name=_('السياسات واللوائح المكتوبة'))
    org_member_with = models.CharField(max_length=100, null=True, blank=True, choices=bool_CHOICES, verbose_name=_(
        'ھل المؤسسة عضو في اي شبكة او تحالف او جسم تنسیقي؟'))
    coalition_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('اسم الشبكة / التحالف'))

    publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        if self.user:
            # return '%s %s' % (self.user.username, self.name)
            # return '%s' % (self.user.username) + ' / ' + '%s' % (self.name)
            return self.user.username

    # def formatted_phone(self, country=None):
    #     return phonenumbers.parse(self.phone, country)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

        img = Image.open(self.logo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # basewidth = 300
            img.thumbnail(output_size)
            # img.thumbnail(basewidth)
            img.save(self.logo.path)
