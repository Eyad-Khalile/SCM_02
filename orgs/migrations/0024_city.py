# Generated by Django 3.1.1 on 2020-10-24 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0023_auto_20201021_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('SY', 'سوريا'), ('IQ', 'العراق'), ('JO', 'اﻷردن'), (
                    'LB', 'لبنان'), ('TR', 'تركيا')], max_length=150, verbose_name='الدولة')),
                ('city_name', models.CharField(
                    max_length=255, verbose_name='اسم المحافظة')),
            ],
        ),
    ]
