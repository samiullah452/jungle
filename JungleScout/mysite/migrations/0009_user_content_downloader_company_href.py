# Generated by Django 2.2.4 on 2019-11-26 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0008_profilemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_content_downloader',
            name='company_href',
            field=models.TextField(default='2'),
            preserve_default=False,
        ),
    ]
