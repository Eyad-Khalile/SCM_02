from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


# https://github.com/akjasim/cb_dj_dependent_dropdown

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


# :::::::::::: CITYES ::::::::::::::::::::::
class City(models.Model):

    country_CHOICES = (
        ('IQ', _('العراق')),
        ('LB', _('لبنان')),
        ('JO', _('اﻷردن')),
        ('SY', _('سوريا')),
        ('TR', _('تركيا')),
    )

    position_work = models.CharField(
        max_length=150, null=False, default=None, choices=country_CHOICES, verbose_name=_('الدولة'))
    city_work = models.CharField(max_length=255, null=False,
                                 verbose_name=_('اسم المحافظة'))

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        if self.city_work:
            return self.city_work


# :::::::::::: ORGS PROFILE ::::::::::::::::::::::
class OrgProfile(models.Model):

    type_CHOICES = (
        ('establishment', _('مؤسسة')),
        ('org', _('جمعية أو منظمة')),
        ('team', _('مبادرة / فريق')),
        ('union', _('اتحاد / تحالف / تجمع')),
        ('group', _('لجنة / تنسيقية / مجموعة'))
    )

    syr_city_CHOICES = (
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

    turky_city_CHOICES = (
        ('Adana', _('أضنة')),
        ('Adıyaman', _('أديامان')),
        ('Afyon', _('أفيون')),
        ('Ağrı', _('أغري')),
        ('Amasya', _('أماسيا')),
        ('Ankara', _('أنقرة')),
        ('Antalya', _('أنطاليا')),
        ('Artvin', _('أرتوين')),
        ('Aydın', _('أيطن')),
        ('Balıkesir', _('بالق أسير')),
        ('Bilecik', _('بيله جك')),
        ('Bingöl', _('بينكُل')),
        ('Bitlis', _('بيطليس')),
        ('Bolu', _('بولو')),
        ('Burdur', _('بوردور')),
        ('Bursa', _('بورصة')),
        ('Çanakkale', _('جاناكالي')),
        ('Çankırı', _('جانقري')),
        ('Çorum', _('جوروم')),
        ('Denizli', _('دنيزلي')),
        ('Diyarbakır', _('ديار بكر')),
        ('Edirne', _('أدرنة')),
        ('Elazığ', _('إلازِغ')),
        ('Erzincan', _('أرزينجان')),
        ('Erzurum', _('أرضروم')),
        ('Eskişehir', _('أسكي شهر')),
        ('Gaziantep', _('غازي عينتاب')),
        ('Giresun', _('غيرسون')),
        ('Gümüşhane', _('كوموش خانة')),
        ('Hakkari', _('حقاري')),
        ('Hattay', _('خطاي')),
        ('Isparta', _('إسبرطة')),
        ('Mersin', _('مرسين')),
        ('İstanbul', _('إسطنبول')),
        ('İzmir', _('إزمير')),
        ('Kars', _('كارس')),
        ('Kastamonu', _('قسطموني')),
        ('Kayseri', _('قيصرية')),
        ('Kırklareli', _('كيركلاريلي')),
        ('Kırşehir', _('قرشهر')),
        ('Kocaeli', _('قوجه ايلي')),
        ('Konya', _('قونية')),
        ('Kütahya', _('كوتاهيا')),
        ('Malatya', _('ملاطية')),
        ('Manisa', _('مانيسا')),
        ('Kahramanmaraş', _('كارامان')),
        ('Mardin', _('ماردين')),
        ('Muğla', _('موغلا')),
        ('Muş', _('موس')),
        ('Nevşehir', _('نوشهر')),
        ('Niğde', _('نيدا')),
        ('Ordu', _('أردو')),
        ('Rize', _('ريزه')),
        ('Sakarya', _('صقاريا')),
        ('Samsun', _('سامسون')),
        ('Siirt', _('سيرت')),
        ('Sinop', _('سينوب')),
        ('Sivas', _('سيواس')),
        ('Tekirdağ', _('تكيرطاغ')),
        ('Tokat', _('توكات')),
        ('Trabzon', _('طرابزون')),
        ('Tunceli', _('تونجلي')),
        ('Şanlıurfa', _('شانلي أورفا')),
        ('Uşak', _('أوشاك')),
        ('Van', _('وان')),
        ('Yozgat', _('يوزكات')),
        ('Zonguldak', _('زونغولداك')),
        ('Aksaray', _('أق سراي')),
        ('Bayburt', _('بايبورت')),
        ('Karaman', _('قرة مان')),
        ('Kırıkkale', _('كيرِك قلعة')),
        ('Batman', _('باتمان')),
        ('Şırnak', _('شرناق')),
        ('Bartın', _('بارتين')),
        ('Ardahan', _('أرض خان')),
        ('Iğdır', _('إغدير')),
        ('Yalova', _('يالوفا')),
        ('Karabük', _('قرة بوك')),
        ('Kilis', _('كيليس')),
        ('Osmaniye', _('عثمانية')),
        ('Düzce', _('دوزجه')),
    )

    jordan_city_CHOICES = (
        ('irbid', _('إربد')),
        ('balka', _('البلقاء')),
        ('jerash', _('جرش')),
        ('zarqa', _('الزرقاء')),
        ('tafilah', _('الطفيلة')),
        ('ajlon', _('عجلون')),
        ('aqaba', _('العقبة')),
        ('amman', _('عمان')),
        ('karak', _('الكرك')),
        ('madaba', _('مادبا')),
        ('ma`an', _('معان')),
        ('mafraq', _('المفرق')),
    )

    liban_city_CHOICES = (
        ('Beirut', _('بيروت')),
        ('Mount Lebanon', _('جبل لبنان')),
        ('North', _('لبنان الشمالي')),
        ('South', _('لبنان الجنوبي')),
        ('Beqaa', _('البقاع')),
        ('Nabatieh', _('النبطية')),
        ('Akkar', _('عكار')),
        ('Baalbek-Hermel', _('بعبلك الهرمل')),
        ('kiserwan', _('كسروان جبيل')),
    )

    iraq_city_CHOICES = (
        ('Erbil', _('أربيل')),
        ('Al Anbar', _('اﻷنبار')),
        ('Babil', _('بابل')),
        ('Baghdad', _('بغداد')),
        ('Basra', _('البصرة')),
        ('Halabja ', _('حلبجة')),
        ('Duhok', _('دهوك')),
        ('Al-Qādisiyyah', _('القادسية')),
        ('Diyala', _('ديالي')),
        ('Dhi Qar', _('ذي قار')),
        ('Sulaymaniyah ', _('السليمانية')),
        ('Saladin', _('صلاح الدين')),
        ('Kirkuk', _('كركوك')),
        ('Karbala', _('كربلاء')),
        ('Muthanna', _('المثنى')),
        ('Maysan', _('ميسان')),
        ('Najaf', _('النجف')),
        ('Nineveh', _('نينوى')),
        ('Wasit', _('واسط')),
    )

    domain_CHOICES = (
        ('Media', _('إعلام')),
        ('Education', _('تعليم')),
        ('Protection', _('حماية')),
        ('Livelihoods and food security', _('سبل العيش واﻷمن الغذائي')),
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
    city_work = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("المحافظة"))
    # city_work = models.CharField(
    #     max_length=150, choices=syr_city_CHOICES, null=True, blank=True, verbose_name=_("المحافظة"))
    logo = models.ImageField(upload_to="org_logos",
                             null=False, default='org_logos/default_logo.jpg', verbose_name=_("شعار المنظمة"))
    message = models.TextField(
        max_length=2000, null=False, verbose_name=_("الرؤية و الرسالة"))

    name_managing_director = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("اسم رئيس مجلس اﻹدارة"))
    name_ceo = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('اسم المدير التنفيذي'))

    # CONTACT INFO
    site_web = models.URLField(
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
    email_person_contact = models.EmailField(
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
    published_at = models.DateTimeField(blank=True, null=True, default=None)
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


# :::::::::::::: ORGS NEWS ::::::::::::::::
class OrgNews(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=False, blank=True)

    title = models.CharField(max_length=255, null=False,
                             verbose_name=_('عنوان الخبر'))
    content = models.TextField(
        max_length=5000, null=False, verbose_name=_('تفاصيل الخبر'))
    image = models.ImageField(upload_to="news_images",
                              null=False, default='news_images/article_img.jpg', verbose_name=_("صورة الخبر"))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

        img = Image.open(self.image.path)

        if img.height > 1000 or img.width > 1000:
            output_size = (1000, 1000)
            # basewidth = 300
            img.thumbnail(output_size)
            # img.thumbnail(basewidth)
            img.save(self.image.path)


# :::::::::: ORGS RAPPORT :::::::::::::::::
class OrgRapport(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=False, blank=True)

    title = models.CharField(max_length=255, null=False,
                             verbose_name=_('عنوان التقرير'))
    media = models.FileField(upload_to="rapport_files",
                             verbose_name=_('صورة او ملف التقرير'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title


class OrgData(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=False, blank=True)

    title = models.CharField(max_length=255, null=False,
                             verbose_name=_('عنوان البيان'))
    media = models.FileField(upload_to="rapport_files",
                             verbose_name=_('صورة او ملف البيان'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title


class OrgMedia(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    org_name = models.ForeignKey(
        OrgProfile, on_delete=models.CASCADE, null=False, blank=True)

    title = models.CharField(max_length=255, null=False,
                             verbose_name=_('عنوان المحتوى'))
    media = models.FileField(upload_to="rapport_files",
                             verbose_name=_('صورة او ملف المحتوى'))
    url = models.URLField(blank=True, max_length=255,
                          null=True, verbose_name=_('رابط المحتوى'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title


class OrgResearch(models.Model):

    domain_CHOICES = (
        ('Media', _('إعلام')),
        ('Education', _('تعليم')),
        ('Protection', _('حماية')),
        ('Livelihoods and food security', _('سبل العيش واﻷمن الغذائي')),
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

    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    # org_name = models.ForeignKey(
    #     OrgProfile, on_delete=models.CASCADE, null=False, blank=True)

    name_entity = models.CharField(
        max_length=255, null=False,  verbose_name=_('اسم الجهة'))

    title = models.CharField(max_length=255, null=False,
                             verbose_name=_('عنوان البحث'))
    domaine = models.CharField(max_length=150, null=False, blank=False,
                               choices=domain_CHOICES, verbose_name=_('مجال البحث'))
    media = models.FileField(upload_to="rapport_files",
                             verbose_name=_('ملف البحث'))
    url = models.URLField(blank=True, max_length=255,
                          null=True, verbose_name=_('رابط البحث'))

    publish = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title
