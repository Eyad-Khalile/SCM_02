# Generated by Django 3.1.1 on 2020-11-05 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0002_auto_20201105_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orgjob',
            old_name='job_city',
            new_name='city_work',
        ),
        migrations.RenameField(
            model_name='orgjob',
            old_name='job_country',
            new_name='position_work',
        ),
    ]