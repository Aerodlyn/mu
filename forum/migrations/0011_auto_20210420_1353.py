# Generated by Django 3.1.8 on 2021-04-20 13:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0010_auto_20210419_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(related_name='memberships', through='forum.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
