# Generated by Django 3.1.1 on 2020-11-07 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0006_auto_20201107_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgjob',
            name='org_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orgs.orgprofile', verbose_name='اسم المنظمة'),
        ),
        migrations.AlterField(
            model_name='otherorgs',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='اضف اسم المنظمة اﻷخرى'),
        ),
    ]