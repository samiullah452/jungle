# Generated by Django 2.2.4 on 2019-12-01 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0014_remove_user_supplier_finder_company_href'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_content_downloader',
            name='company_href',
        ),
    ]