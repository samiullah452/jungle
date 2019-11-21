# Generated by Django 2.2.4 on 2019-11-20 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mysite', '0002_supplier_finder_groups_supplier_finder_image_user_supplier_finder'),
    ]

    operations = [
        migrations.CreateModel(
            name='keyword_groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='user_keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('category_name', models.TextField()),
                ('product_name', models.TextField()),
                ('category_id', models.TextField()),
                ('keywords', models.TextField()),
                ('details', models.TextField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.keyword_groups')),
            ],
        ),
    ]