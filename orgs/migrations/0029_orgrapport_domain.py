# Generated by Django 3.1.1 on 2020-10-27 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0028_auto_20201024_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgrapport',
            name='domain',
            field=models.CharField(choices=[('Media', 'إعلام'), ('Education', 'تعليم'), ('Protection', 'حماية'), ('Livelihoods and food security', 'سبل العيش واﻷمن الغذائي'), ('Project of clean ,water, sanitation ', 'مشاريع النظافة والمياه والصرف الصحي'), ('Development', 'تنمية'), ('Law, suport, policy', 'قانون و مناصرة و سیاسة'), ('Donors and support volunteering', 'مانحین و دعم العمل التطوعي'), ('Religious org', 'منظمات دینیة'), ('Prof association and assembles', 'تجمعات و اتحادات مھنیة'), ('Health', 'صحة'), ('Studies and research', 'دراسات وأبحاث'), ('Other', 'أخرى')], default='Other', max_length=150, verbose_name='مجال التقرير'),
        ),
    ]
