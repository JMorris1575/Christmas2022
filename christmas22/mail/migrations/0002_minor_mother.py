# Generated by Django 3.2.9 on 2021-12-10 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='minor',
            name='mother',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='mother_of_minor', to='auth.user'),
            preserve_default=False,
        ),
    ]
