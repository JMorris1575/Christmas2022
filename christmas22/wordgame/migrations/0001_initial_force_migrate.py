# Generated by Django 3.1.3 on 2020-11-28 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChristmasWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=25)),
                ('sequence_number', models.IntegerField(unique=True)),
                ('date_published', models.DateField(default=django.utils.timezone.now)),
                ('finalized', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['sequence_number'],
            },
        ),
        migrations.CreateModel(
            name='PlayerWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=25)),
                ('score', models.IntegerField(default=0)),
                ('explanation', models.CharField(blank=True, default='', max_length=50)),
                ('start_word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wordgame.christmasword')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
