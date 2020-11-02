# Generated by Django 3.1.1 on 2020-10-27 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0026_auto_20201027_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgfundingopp',
            name='funding_amounte',
            field=models.CharField(blank=True, choices=[('less than 5000 ', 'أقل من 5000 دولار'), ('from 5000 to 10000 dollar', 'بين 5000 و 10000 دولار'), ('from 10000 to 50000', 'بين 10000 و50000 دولار'), ('from 50000 to 100000', 'بين 50000 و100000 دولار'), ('more than  100000', 'بين 50000 و100000 دولار'), ('other', 'أخرى')], max_length=255, null=True, verbose_name=' حجم المنحة'),
        ),
        migrations.AlterField(
            model_name='orgfundingopp',
            name='funding_period',
            field=models.CharField(blank=True, choices=[('less of 6 months', 'أقل من 6 أشهر'), ('from 6 mths to one year', 'ستة أشهر لسنة'), ('from one to 2 years', 'سنة إلى سنتين'), ('more than 2 years', 'أكثر من سنتين'), ('other', 'أخرى')], max_length=255, null=True, verbose_name='مدة المنحة'),
        ),
    ]
