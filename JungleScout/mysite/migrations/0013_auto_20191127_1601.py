# Generated by Django 2.2.4 on 2019-11-27 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0012_auto_20191127_1520'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_supplier_finder',
            old_name='details',
            new_name='region',
        ),
    ]
