# Generated by Django 3.1.1 on 2020-11-07 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0007_auto_20201107_1425'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orgjob',
            old_name='other_org_name',
            new_name='other_name',
        ),
        migrations.RenameField(
            model_name='otherorgs',
            old_name='name',
            new_name='other_name',
        ),
    ]