# Generated by Django 4.0.4 on 2022-07-28 14:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_user_followers_alter_user_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, default=None, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, default=None, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
