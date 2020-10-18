# Generated by Django 3.1.1 on 2020-10-16 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0015_orgrapport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgnews',
            name='org_name',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='orgs.orgprofile'),
        ),
        migrations.AlterField(
            model_name='orgrapport',
            name='org_name',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='orgs.orgprofile'),
        ),
    ]