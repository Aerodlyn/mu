# Generated by Django 3.1.8 on 2021-04-16 23:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import forum.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0006_post_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='name',
            field=models.CharField(max_length=64, primary_key=True, serialize=False, validators=[forum.validators.ValidateAgainstBlacklist(['all', 'new'])]),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.community')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(related_name='members', through='forum.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]