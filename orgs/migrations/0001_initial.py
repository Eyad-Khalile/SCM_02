# Generated by Django 2.2.12 on 2020-09-18 08:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_confirmed', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255, verbose_name='اسم المنظمة')),
                ('name_en_ku', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المنظمة باللغة الانكليزية أو الكردية')),
                ('short_cut', models.CharField(blank=True, max_length=255, null=True, verbose_name='الاسم المختصر')),
                ('org_type', models.CharField(choices=[('establishment', 'مؤسسة'), ('org', 'جمعية أو منظمة'), ('team', 'مبادرة / فريق'), ('union', 'اتحاد / تحالف / تجمع'), ('group', 'لجنة / تنسيقية / مجموعة')], max_length=150, verbose_name='نوع المنظمة')),
                ('position_work', django_countries.fields.CountryField(max_length=255, verbose_name='مكان العمل')),
                ('city_work', models.CharField(blank=True, choices=[('aleppo', 'حلب'), ('damascus', 'دمشق'), ('suburb of damascus', 'ريف دمشق'), ('daraa', 'درعا'), ('deir ez-Zor', 'دير الزور'), ('hama', 'حماه'), ('al-Hasakah', 'الحسكة'), ('homs', 'حمص'), ('idlib', 'إدلب'), ('latakia', 'اللاذقية'), ('quneitra', 'القنيطرة'), ('raqqa', 'الرقة'), ('as-Suwayda', 'السويداء'), ('tartus', 'طرطوس')], max_length=150, null=True, verbose_name='المحافظة')),
                ('logo', models.ImageField(default='org_logos/default_logo.jpg', upload_to='org_logos', verbose_name='شعار المنظمة')),
                ('message', models.TextField(max_length=2000, verbose_name='الرؤية و الرسالة')),
                ('name_managing_director', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم رئيس مجلس اﻹدارة')),
                ('name_ceo', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المدير التنفيذي')),
                ('site_web', models.CharField(blank=True, max_length=255, null=True, verbose_name='الموقع الالكتروني')),
                ('facebook', models.URLField(blank=True, max_length=255, null=True, verbose_name='صفحة فيسبوك')),
                ('twitter', models.URLField(blank=True, max_length=255, null=True, verbose_name='صفحة تويتر')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='البريد الاكتروني')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='رقم الهاتف')),
                ('name_person_contact', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم الشخص المسؤول عن التواصل')),
                ('email_person_contact', models.CharField(blank=True, max_length=255, null=True, verbose_name='البريد الاكتروني للشخص المسؤول عن التواصل')),
                ('work_domain', models.CharField(choices=[('Media', 'إعلام'), ('Education', 'تعليم'), ('Protection', 'حماية'), ('Livelihoods and food security', 'سبل العيش والأمن الغذائي'), ('Project of clean ,water, sanitation ', 'مشاريع النظافة والمياه والصرف الصحي'), ('Development', 'تنمية'), ('Law, suport, policy', 'قانون و مناصرة و سیاسة'), ('Donors and support volunteering', 'مانحین و دعم العمل التطوعي'), ('Religious org', 'منظمات دینیة'), ('Prof association and assembles', 'تجمعات و اتحادات مھنیة'), ('Health', 'صحة'), ('Studies and research', 'دراسات وأبحاث'), ('Other', 'أخرى')], max_length=255, verbose_name='مجال العمل')),
                ('target_cat', models.CharField(choices=[('No category selected', 'لا يوجد فئة محددة'), ('womans', 'نساء'), ('Mans', 'رجال'), ('Youth 18-24', 'شباب 18-24'), ('Child 0-18', 'أطفال 0-18'), ('Religious groups', 'مجموعات دینیة'), ('Ethnic groups', 'مجموعة عرقیة'), ('Persons lacking breadwinner ', 'فاقدي المعیل'), ('Handicapped', 'ذوي الاحتیاجات الخاصة'), ('Refugees', 'لاجئین'), ('Displaced', 'نازحین'), ('Returned', 'عائدین'), ('Other civil society organizations', 'منظمات مجتمع مدني اخرى'), ('Other', 'أخرى')], max_length=255, verbose_name='الفئات المستهدفة')),
                ('date_of_establishment', models.DateField(blank=True, max_length=150, null=True, verbose_name='تاريخ التأسيس')),
                ('is_org_registered', models.CharField(choices=[('0', 'لا'), ('1', 'نعم')], max_length=100, verbose_name='هل المنظمة مسجلة ؟')),
                ('org_registered_country', django_countries.fields.CountryField(blank=True, max_length=255, null=True, verbose_name='بلد التسجيل')),
                ('org_adress', models.CharField(max_length=255, verbose_name='عنوان المقر الرئيسي')),
                ('org_members_count', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='عدد اﻷعضاء')),
                ('org_members_womans_count', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='عدد النساء من اﻷعضاء')),
                ('w_polic_regulations', models.CharField(choices=[('No', 'لا يوجد'), ('Code of conduct', 'مدونة السلوك'), ('Child protection', 'حماية الطفل'), ('Anti-corruption', 'مكافحة الفساد'), ('Human resources policy', 'سياسة الموارد البشرية'), ('Procurement policy', 'سياسة المشتريات'), ('Volunteering policy', 'سياسة التطوع'), ('Anti-harassment Policy', 'سياسة منع التحرش'), ('Financial policy', 'السياسة المالية'), ('Equipment use Policy', 'سياسة استخدام المعدات'), ('privacy policy', 'سياسة الخصوصية'), ('Other', 'أخرى')], max_length=200, verbose_name='السياسات واللوائح المكتوبة')),
                ('org_member_with', models.CharField(blank=True, choices=[('0', 'لا'), ('1', 'نعم')], max_length=100, null=True, verbose_name='ھل المؤسسة عضو في اي شبكة او تحالف او جسم تنسیقي؟')),
                ('coalition_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم الشبكة / التحالف')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
