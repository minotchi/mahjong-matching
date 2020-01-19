# Generated by Django 2.1.2 on 2020-01-13 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0007_room_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='更新時間'),
        ),
        migrations.AddField(
            model_name='room',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
    ]
