# Generated by Django 2.1.2 on 2020-03-20 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_oshihiki_is_dora'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hora_value_index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(verbose_name='和了価値指標')),
                ('rule', models.IntegerField(verbose_name='ルール')),
                ('ba', models.IntegerField(verbose_name='場')),
                ('own_point', models.FloatField(verbose_name='自分の持ち点')),
            ],
        ),
    ]
