# Generated by Django 2.2.12 on 2020-09-20 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0006_auto_20200920_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgprofile',
            name='logo',
            field=models.ImageField(default='org_logos/default_logo.jpg', upload_to='\\SCM-02\new_venv\\scm\\media\\org_logos', verbose_name='شعار المنظمة'),
        ),
    ]