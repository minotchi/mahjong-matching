# Generated by Django 2.1.2 on 2020-03-15 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_oshihiki'),
    ]

    operations = [
        migrations.AddField(
            model_name='oshihiki',
            name='hoju_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='放銃率'),
        ),
        migrations.AddField(
            model_name='oshihiki',
            name='junme',
            field=models.IntegerField(blank=True, null=True, verbose_name='順目'),
        ),
        migrations.AddField(
            model_name='oshihiki',
            name='oponent_is_parent',
            field=models.BooleanField(default=False, editable=False, verbose_name='相手'),
        ),
        migrations.AddField(
            model_name='oshihiki',
            name='you_are_parent',
            field=models.BooleanField(default=False, editable=False, verbose_name='自分'),
        ),
    ]