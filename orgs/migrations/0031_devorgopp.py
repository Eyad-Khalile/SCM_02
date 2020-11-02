# Generated by Django 3.1.1 on 2020-10-28 01:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orgs', '0030_orgcapacityopp'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevOrgOpp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_dev', models.CharField(max_length=255, verbose_name='عنوان المادة')),
                ('dev_date', models.DateTimeField(blank=True, null=True, verbose_name='تاريخ الإعداد/النشر/التأليف')),
                ('name_dev', models.CharField(max_length=255, verbose_name='اسم الجهة ')),
                ('dev_description', models.TextField(max_length=2000, verbose_name='لمحة عن الجهة')),
                ('publish', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('updated_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('org_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orgs.orgprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
