# Generated by Django 3.1.7 on 2021-04-01 22:20

from django.db import migrations, models
import forum.models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20210401_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=forum.models.community_directory_path),
        ),
    ]
