# Generated by Django 2.2.4 on 2019-11-27 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0010_auto_20191127_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_content_downloader',
            name='price_krw',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
