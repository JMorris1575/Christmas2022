# Generated by Django 2.1.3 on 2018-12-09 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trivia', '0002_auto_20181206_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triviaquestion',
            name='explanation',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
