# Generated by Django 4.1.9 on 2023-05-30 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("votes", "0003_alter_vote_menu"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vote",
            name="user",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
