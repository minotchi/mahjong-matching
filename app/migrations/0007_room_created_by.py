# Generated by Django 2.1.2 on 2020-01-13 14:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_room_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_created_by', to=settings.AUTH_USER_MODEL, verbose_name='作成者'),
        ),
    ]
