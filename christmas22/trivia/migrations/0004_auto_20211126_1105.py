# Generated by Django 3.2.9 on 2021-11-26 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trivia', '0003_auto_20181209_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triviachoice',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='triviaconversation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='triviaquestion',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='triviaresponse',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
