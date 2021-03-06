# Generated by Django 3.1.3 on 2020-12-26 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wordgame', '0002_wordcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordcomment',
            name='comment',
            field=models.CharField(max_length=512),
        ),
        migrations.CreateModel(
            name='GameComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=512)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
