# Generated by Django 3.1.7 on 2021-04-01 00:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import forum.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0002_auto_20210327_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='community',
            name='name',
            field=models.CharField(max_length=64, primary_key=True, serialize=False, validators=[forum.validators.ValidateAgainstBlacklist(['new'])]),
        ),
    ]